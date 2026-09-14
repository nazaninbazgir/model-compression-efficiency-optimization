# Data placement

Original HODA data remains locally in `data/raw/hoda/`:

- `Train 60000.cdb`: training split used by notebook 01.
- `Test 20000.cdb`: test split used by notebook 01 and checkpoint validation.
- `RemainingSamples.cdb`: preserved, unused by the supplied experiments.

The `.cdb` basenames are intentionally retained to match the distributed data. For a new clone, obtain the HODA files from the [HODA Dataset Reader source repository](https://github.com/amir-saniyan/HodaDatasetReader) and place them here. The local project did not include redistribution/license documentation for these files; they are excluded from Git, not deleted.

Fashion-MNIST downloads to `data/raw/` when notebook 02 runs. IMDB and the BERT tokenizer download to the normal Hugging Face cache. They were not included in the original folder. The offline smoke tests use generated fixtures for these two tasks, not downloaded evaluation datasets.
