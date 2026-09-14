# Preserved HODA checkpoints

`mlp_weights.pth` is the state dictionary used by the portable Fashion-MNIST notebook and validation script. `mlp_model.pth` is the original full serialized model and remains preserved locally for provenance, but is excluded from Git as a redundant artifact. Neither is overwritten by notebook 01; new checkpoints go to `outputs/`.

Architecture: Flatten â†’ Linear(1024, 200) â†’ ReLU â†’ Linear(200, 150) â†’ ReLU â†’ Linear(150, 10), with 236,660 trainable parameters.

The full-object checkpoint is redundant for the documented execution workflow, but has not been deleted. Only load checkpoints whose provenance you trust.
