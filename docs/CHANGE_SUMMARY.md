# GitHub preparation summary

## Preserved originals

All 14 supplied files are accounted for in `original_file_manifest.json`. Nothing was deleted. Original notebook bytes were moved into the ignored local `archive/originals/` directory before making portable copies. Data, reader code and both model files remain byte-identical. The original report is preserved in the ignored archive; its public copy has been restored byte-for-byte, including its original title page.

## Names and structure applied

| Original | New location |
|---|---|
| `1/Math4AI_Project_1.ipynb` | `notebooks/01_hoda_mlp_svd.ipynb` (portable copy) |
| `2/Math4AI_Project_2.ipynb` | `notebooks/02_fashion_mnist_lora.ipynb` (portable copy) |
| `3/Math4AI_Project_3_1.ipynb` | `notebooks/03_imdb_transformer_baseline.ipynb` (portable copy) |
| `3/Math4AI_Project_3_2.ipynb` | `notebooks/04_imdb_transformer_svd.ipynb` (portable copy) |
| `1/HodaDatasetReader.py` | `src/HodaDatasetReader.py` |
| `1/mlp_model.pth`, `1/mlp_weights.pth` | `models/` with original basenames |
| `hoda/*.cdb` | `data/raw/hoda/` with original basenames |
| `Math4AI 4031 - Final Project.pdf` | `docs/project_assignment.pdf` |
| `Mathematics_for_AI___Final_Project.pdf` | `docs/project_report.pdf` (original cover restored; backup archived) |

The original numerical directories are left as empty local directories; Git does not track empty directories. `HodaDatasetReader.py` keeps its original name to preserve attribution and imports. A possible later name is `hoda_reader.py`, but it is unnecessary for this cleanup.

## Added and changed

- English portfolio README with methods, datasets, execution instructions, results and limitations.
- Pinned direct dependencies in `requirements.txt` and binary/text rules in `.gitattributes`.
- `.gitignore` covering environments, caches, raw data, original local archives and new run outputs. Saved notebook outputs and the required state dictionary are retained for publication; the redundant full-object checkpoint is local-only.
- Four portable notebooks with original historical outputs intact; local path setup, removed Colab-only setup, guarded GPU telemetry and state-dictionary loading. Exact source edits remain locally in the ignored `notebook_portability_changes.json`.
- Historical metrics and figures in `results/`; duplicate text extracts are local-only.
- Offline notebook execution and full HODA checkpoint validation in `scripts/validate_project.py`.
- Preservation, data, model, reproducibility and validation documentation.

## Extra or non-runnable files identified, not deleted

| Item | Assessment | Treatment |
|---|---|---|
| `confusion and curves.ipynb` | Corrupted JSON/binary tail; cannot execute | Exact original in local archive |
| `Transformer-SVD.ipynb` | Assignment starter with TODOs | Exact original in local archive |
| `mlp_model.pth` | Redundant full-object checkpoint for current workflow | Kept under `models/`, ignored by Git |
| `RemainingSamples.cdb` | Unused by experiment code | Kept under ignored raw data |
| `.review/`, `.venv/`, `outputs/validation/` | Generated review, environment and test artifacts | Ignored by Git; retained locally |

## Publication state

The reviewed project is prepared for initial publication on `main`. The final publication contents and checks are recorded in `PUBLICATION_REVIEW.md` and `VALIDATION.md`. Raw HODA data and local original notebook backups will not be included by a normal `git add`; keep a separate backup of them. No project or third-party license was invented.

## Final publication review

See [PUBLICATION_REVIEW.md](PUBLICATION_REVIEW.md). The final publication set excludes the original assignment PDF, redundant full-object model, duplicate text logs and raw portability diff. At the author's final request, the original report cover, including course title, university and date, has been restored. All original files remain available locally.
