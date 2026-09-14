# Validation results

Validated locally on **2026-09-14** using **Windows, Python 3.13.9, PyTorch 2.8.0+cpu and torchvision 0.23.0+cpu**. The installed package snapshot is in [validation_environment.txt](validation_environment.txt), and machine-readable results are in [validation_results.json](validation_results.json).

## Passed checks

| Check | Result |
|---|---|
| Original-file preservation | SHA-256 matches for all 14 supplied files |
| Historical notebook outputs | All cell outputs unchanged in the four portable copies |
| Notebook format and rendering | All four validate as nbformat 4.5 and export to HTML |
| Dependency consistency | `python -m pip check`: no broken requirements |
| Model loading | Supplied full-model and state-dictionary tensors are identical |
| HODA checkpoint evaluation | **19,656 / 20,000 correct: 98.28% accuracy** |
| HODA MLP/SVD notebook | All cells executed without an error output |
| Fashion-MNIST LoRA notebook | All cells executed without an error output |
| IMDB baseline notebook | All cells executed without an error output |
| IMDB SVD notebook | All cells executed without an error output after the logging-only scheduler compatibility fix |

## Execution scope

The notebook tests run every code cell, including training, evaluation, plotting and checkpoint operations. They use **one epoch**, **ranks 1 and 10** where applicable, **64 real HODA training/test examples**, **64/32 generated image examples** for the Fashion-MNIST pipeline, and **eight generated text examples per split** with a local miniature BERT tokenizer and sequence length 16 for the Transformer pipelines. HODA preprocessing reads the supplied complete training/test files before selecting the test subsets. The standalone checkpoint evaluation uses the entire HODA test split.

The first three notebooks passed in the initial execution run. The fourth exposed an unsupported `ReduceLROnPlateau(verbose=True)` argument; removing that logging argument retained all scheduling settings. The fourth notebook was rerun successfully. Original outputs were not replaced by test results.

Commands used:

```bash
python scripts/validate_project.py --evaluate --smoke
python scripts/validate_project.py --evaluate --smoke --notebook 04_imdb_transformer_svd.ipynb
python -m pip check
```

The first command identified the scheduler compatibility issue; the targeted second command verified its correction. All four executed notebooks are retained locally in `outputs/validation/`. Run the first command again to repeat the complete smoke suite on the final source.

## Limits

- Full original epoch/rank sweeps were not retrained. Only the saved HODA checkpoint's full test accuracy was independently reproduced.
- Tests did not download Fashion-MNIST, IMDB, or the public pretrained tokenizer. Those network-dependent paths were replaced only in the in-memory test copies.
- Tests used CPU, not CUDA; historical GPU time and memory metrics were not reproduced.
- Jupyter emitted a non-fatal Windows event-loop fallback warning. It did not prevent notebook execution.
- The corrupted supplementary plotting notebook and incomplete starter template are preserved, documented, and excluded from the runnable experiment set.
- Scientific issues already present in the training procedures are documented in [REPRODUCIBILITY.md](REPRODUCIBILITY.md); these runtime checks do not remove those limitations.

## Publication-only update

The full-object checkpoint is now optional in the validation script because it is excluded from Git. Its tensor comparison is performed when the local file exists and otherwise reported as `null`, not a pass. The entire public report was restored byte-for-byte from the archived original, including the original cover. These changes do not alter notebook training or results.
