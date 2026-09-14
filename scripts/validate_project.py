"""Validate artifacts and run every experiment notebook with small offline fixtures.

The reduced runs test execution, not reproduction of published metrics.
Original notebooks, checkpoints and historical outputs are never overwritten.
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def validate_originals():
    manifest = json.loads((ROOT / "docs/original_file_manifest.json").read_text())
    checked = 0
    missing = []
    for item in manifest:
        path = ROOT / item["preserved_path"]
        if not path.exists():
            missing.append(item["preserved_path"])
            continue
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item["sha256"], path
        checked += 1
    return {"verified": checked, "absent_optional_originals": missing}


def smoke_notebooks(selected=None):
    import nbformat
    from nbclient import NotebookClient

    destination = ROOT / "outputs/validation"
    destination.mkdir(parents=True, exist_ok=True)
    results = []
    for path in sorted((ROOT / "notebooks").glob("*.ipynb")):
        if selected and path.name != selected:
            continue
        notebook = nbformat.read(path, as_version=4)
        nbformat.validate(notebook)
        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue
            source = cell.source
            compile(source, str(path), "exec")
            # Scope these overrides to the in-memory test copy only.
            source = source.replace('ROOT / "outputs"', 'ROOT / "outputs/validation/checkpoints"')
            source = source.replace('OUTPUT_DIR.mkdir(exist_ok=True)', 'OUTPUT_DIR.mkdir(parents=True, exist_ok=True)')
            source = re.sub(r"num_epochs\s*=\s*\d+", "num_epochs=1", source)
            source = re.sub(r"(k_values|rank_values|lowRank_values) = \[[^\]]+\]", r"\1 = [1, 10]", source)
            source = source.replace('X_train_tensor = torch.tensor(X_train,', 'X_train_tensor = torch.tensor(X_train[:64],')
            source = source.replace('Y_train_tensor = torch.tensor(Y_train,', 'Y_train_tensor = torch.tensor(Y_train[:64],')
            source = source.replace('X_test_tensor = torch.tensor(X_test,', 'X_test_tensor = torch.tensor(X_test[:64],')
            source = source.replace('Y_test_tensor = torch.tensor(Y_test,', 'Y_test_tensor = torch.tensor(Y_test[:64],')
            if 'train_dataset = torchvision.datasets.FashionMNIST(' in source:
                start = source.index('# Load Fashion MNIST dataset')
                source = source[:start] + '''# Offline image fixture; not Fashion-MNIST evaluation.
train_dataset = torchvision.datasets.FakeData(size=64, image_size=(1, 28, 28), num_classes=10, transform=transform)
test_dataset = torchvision.datasets.FakeData(size=32, image_size=(1, 28, 28), num_classes=10, transform=transform, random_offset=64)
'''
            if 'dataset = load_dataset("imdb")' in source:
                source = '''from datasets import Dataset, DatasetDict
fixture = Dataset.from_dict({"text": ["a good movie", "a bad movie"] * 4, "label": [1, 0] * 4})
dataset = DatasetDict(train=fixture, test=fixture)
train_data, test_data = dataset["train"], dataset["test"]
'''
            if 'tokenizer = BertTokenizer.from_pretrained(' in source:
                source = '''vocab_file = OUTPUT_DIR / "smoke_vocab.txt"
vocab_file.write_text("[PAD]\\n[UNK]\\n[CLS]\\n[SEP]\\n[MASK]\\na\\ngood\\nbad\\nmovie\\n", encoding="utf-8")
tokenizer = BertTokenizer(vocab_file=str(vocab_file))
'''
            source = source.replace('max_seq_length = 512', 'max_seq_length = 16')
            # Use an inline backend so all plotting cells are exercised without windows.
            cell.source = source
            cell.outputs = []
            cell.execution_count = None
        setup = nbformat.v4.new_code_cell("import torch\ntorch.set_num_threads(2)\n%matplotlib inline")
        notebook.cells.insert(0, setup)
        print(f"Executing {path.name}", flush=True)
        NotebookClient(notebook, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(ROOT)}}).execute()
        nbformat.write(notebook, destination / path.name)
        results.append({"notebook": path.name, "status": "passed", "scope": "all cells, one epoch, reduced offline fixtures; ranks 1 and 10"})
    return results


def evaluate_checkpoint():
    import torch
    import nbformat
    import ast
    from HodaDatasetReader import read_hoda_dataset

    torch.set_num_threads(2)
    namespace = {"nn": torch.nn}
    nb = nbformat.read(ROOT / "notebooks/01_hoda_mlp_svd.ipynb", as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "code":
            for node in ast.parse(cell.source).body:
                if isinstance(node, ast.ClassDef) and node.name == "Model":
                    exec(compile(ast.Module(body=[node], type_ignores=[]), "notebook Model", "exec"), namespace)
    model = namespace["Model"]()
    model.load_state_dict(torch.load(ROOT / "models/mlp_weights.pth", map_location="cpu", weights_only=True))
    # Inspect only the known original architecture, without unrestricted unpickling.
    full_model_matches = None
    if (ROOT / "models/mlp_model.pth").exists():
        allowed = [(namespace["Model"], "__main__.Model"), torch.nn.Flatten, torch.nn.Linear, torch.nn.ReLU, set]
        with torch.serialization.safe_globals(allowed):
            original_model = torch.load(ROOT / "models/mlp_model.pth", map_location="cpu", weights_only=True)
        assert model.state_dict().keys() == original_model.state_dict().keys()
        assert all(torch.equal(value, original_model.state_dict()[key]) for key, value in model.state_dict().items())
        full_model_matches = True
    model.eval()
    images, labels = read_hoda_dataset(str(ROOT / "data/raw/hoda/Test 20000.cdb"))
    assert images.shape == (20000, 1024)
    assert set(labels.tolist()) == set(range(10))
    correct = 0
    with torch.no_grad():
        for i in range(0, len(images), 256):
            logits = model(torch.from_numpy(images[i:i+256]))
            assert torch.isfinite(logits).all()
            correct += int((logits.argmax(1) == torch.from_numpy(labels[i:i+256])).sum())
    return {"samples": len(images), "correct": correct, "accuracy_percent": correct / len(images) * 100, "full_model_and_state_dict_identical": full_model_matches}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="execute all four notebooks with offline test fixtures")
    parser.add_argument("--evaluate", action="store_true", help="evaluate the preserved checkpoint on all 20,000 HODA test samples")
    parser.add_argument("--notebook", choices=sorted(p.name for p in (ROOT / "notebooks").glob("*.ipynb")), help="restrict --smoke to one notebook")
    args = parser.parse_args()
    report = {"original_files": validate_originals()}
    if args.evaluate:
        report["hoda_checkpoint"] = evaluate_checkpoint()
    if args.smoke:
        report["notebooks"] = smoke_notebooks(args.notebook)
    target = ROOT / "outputs/validation"
    target.mkdir(parents=True, exist_ok=True)
    (target / "validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
