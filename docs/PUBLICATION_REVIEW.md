# Final publication review

## Privacy and credentials

- Gitleaks v8.30.1 (official release archive checked against its published SHA-256 checksum) found no secrets in the publication candidate. Extracted PDF text was scanned separately.
- Additional pattern checks covered notebook source, text/HTML outputs, widget metadata, configuration/documentation, and checkpoint archive metadata. No credential tokens, secret assignments, private keys, credential-bearing URLs, email addresses or personal filesystem paths were detected in the final publication set.
- PDF pages, metadata, annotations and attachments were inspected. The original report metadata contains document-production details and timestamps; its original academic title page is intentionally retained. The report has no external links. Figure metadata contains only rendering software and resolution information.
- At the author's final request, the original report title page is retained with the author name, course title, university and date. The complete published PDF matches the preserved original SHA-256. The README introduction remains concise.

Automated secret detection is pattern-based and cannot prove the absence of every possible secret. These findings apply to the reviewed files, not to future additions.

## Retained for publication

The four experiment notebooks, their historical outputs, report, required HODA state dictionary, reader, requirements, validation utility, historical metrics/figures and project documentation remain in the publication set. The report's **45 body pages are pixel-identical to the original**; page content streams and annotation counts were also checked.

The largest file is `notebooks/02_fashion_mnist_lora.ipynb` at **1,786,290 bytes (1.79 MB)**. No publication file exceeds 2 MB. The complete staged content is approximately **6.28 MB**, before Git compression. The model state dictionary is about 0.95 MB and is needed for reproducible inference and LoRA initialization.

## Preserved locally, excluded from Git

| File or directory | Reason |
|---|---|
| `data/raw/` | Raw datasets/downloads |
| `archive/originals/` | Original notebook backups and unedited report |
| `models/mlp_model.pth` | Redundant full-object model; the state dictionary suffices |
| `docs/project_assignment.pdf` | Not needed to run/review the experiments; contains third-party names and a Drive link |
| `docs/notebook_portability_changes.json` | Internal before/after log containing old Colab paths |
| `results/*_historical.txt` | Duplicate text logs; the outputs remain in notebooks |
| `.review/`, `.venv/`, `outputs/validation/` | Local audit tools, environment and test artifacts |
| Credential file patterns in `.gitignore` | Prevent accidental addition of common local secrets |

No original file or dataset was deleted. Original hashes remain recorded in `original_file_manifest.json`; the unedited report's preserved path now points into the local archive.

## Runtime verification after exclusions

The publication candidate was tested without `mlp_model.pth`. Its validation script loaded only `mlp_weights.pth` and again classified **19,656 of 20,000 HODA test samples correctly (98.28%)**. The optional full-model comparison reports `null` when that local-only file is absent. Notebook sources and historical outputs are unchanged by this publication audit; their earlier execution checks remain documented in `VALIDATION.md`.

## Git state

The reviewed files form the initial publication on `main`. Inspect repository content and history with:

```bash
git diff --cached --stat
git diff --cached
git status --short
```
