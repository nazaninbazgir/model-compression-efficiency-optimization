# Historical experiment outputs

These artifacts are extracted from the supplied notebooks, with no retraining or recomputation:

- `*_historical.txt`: duplicate local text extracts; excluded from Git. The same historical outputs remain in the notebooks.
- `figures/*.png`: the last saved PNG figure from each experiment notebook.
- `historical_rank_metrics.json`: the eight HODA SVD and nine IMDB SVD rows extracted from the saved text tables, with notebook provenance.

All original embedded outputs remain in the portable notebooks. The complete source notebooks also remain locally in `archive/originals/`.

Resource measurements use the original notebook-specific conventions and hardware. Do not combine GPU memory columns across experiments as if they measured the same quantity. New validation output is kept separately under `outputs/validation/`; see `docs/VALIDATION.md` for the published validation summary.
