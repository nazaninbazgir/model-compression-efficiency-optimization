# Reproducibility and scientific scope

The four portable notebooks preserve the experiment code, hyperparameters and historical outputs, except for documented filesystem/runtime compatibility changes. Cell-level before/after source is recorded locally in the ignored `notebook_portability_changes.json`; the unmodified sources remain in the local archive.

## Runtime changes

- Replace Colab Drive mounting and shell copy/install commands with repository-relative paths and `requirements.txt`.
- Save newly trained HODA checkpoints under `outputs/`, keeping supplied models intact.
- Load the provided state dictionary with `weights_only=True` into the same MLP architecture instead of relying on full-object unpickling in Fashion-MNIST.
- Guard CUDA memory-reset and memory-query calls when CUDA is unavailable. CPU memory values are not equivalent to GPU measurements.
- Remove the unsupported `verbose=True` logging argument from the SVD Transformer's `ReduceLROnPlateau` scheduler. All learning-rate scheduling parameters are unchanged.
- Add deterministic cell identifiers for notebook format compatibility. No random seed is imposed on the original training procedures.
- Wrap Colab's saved widget dictionaries in the standard versioned `state` envelope for notebook/GitHub rendering. The underlying widget states and all cell outputs remain unchanged.

## Original scientific limitations retained

1. SVD-MLP factors are initialized from random matrices, rather than decomposing the trained baseline checkpoint. The factorized model omits biases and applies Softmax before CrossEntropyLoss; the baseline uses biases and logits. This is not an isolated post-training compression comparison.
2. In the Transformer training loops, `model.train()` is called before the epoch loop and evaluation switches to `eval()` without restoring training mode. Subsequent epochs therefore retain evaluation mode (including disabled dropout). Fixing this would change training behavior and requires a new experiment; it was deliberately not changed.
3. Transformer classifiers do not use the token attention mask and average over padded positions. This behavior was retained.
4. The baseline Transformer uses two layers, eight heads, five epochs and learning rate `3e-4`; the SVD variant uses one layer, four heads, ten epochs and learning rate `2e-5`. The SVD attention also lacks the baseline output projection. Parameter and timing differences cannot be attributed solely to SVD.
5. The saved baseline tokenizer example contains 256 tokens while the current source sets 512. Historical output and source may reflect different interactive runs. The report and notebook results are retained as recorded, without claiming exact fresh-kernel reproduction.
6. No controlled seed/repeated-run uncertainty estimates or validation split are defined. Rank comparisons use the test split. Reported numbers should not be presented as an unbiased benchmark of rank selection.
7. LoRA retains the frozen pretrained model. Trainable parameter savings do not imply the same reduction in total storage or inference cost. Some high ranks exceed the baseline trainable parameter count.
8. GPU memory measurements use differing allocated/reserved/peak conventions and include other live objects. They are not isolated per-model footprints. CPU fallback values do not measure process RAM.
9. The baseline and LoRA learning-curve function labels accuracy as percent while its training values are fractions. Original plots are preserved without rescaling the historical outputs.

The purpose of the cleanup is a reviewable portfolio repository, not a new scientific result. Full original rank sweeps must be rerun separately to produce new measurements. Any methodological correction should be developed as a separately documented experiment.
