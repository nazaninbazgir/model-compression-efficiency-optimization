# Local original notebook archive

`originals/` contains the exact original notebooks and is excluded from Git. Paths and checksums are in `docs/original_file_manifest.json`.

- `1/confusion and curves.ipynb` has binary corruption beginning at byte offset 1,220,608 inside an encoded plot and an invalid/truncated JSON tail. It cannot be opened as a valid notebook. No reconstructed output is presented as authentic.
- `3/Transformer-SVD.ipynb` is a starter template with TODOs and undefined configuration variables, not a completed experiment.
- The other four notebooks are preserved originals of the portable notebooks under `notebooks/`.

These files are not disposable originals. Keep a backup of this directory before sharing only the Git-tracked project.
