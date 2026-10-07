# Attribution

## Upstream project
- **Project:** emlearn — ML inference in C for microcontrollers
- **Author/maintainer:** Jon Nordby and contributors
- **Source:** https://github.com/emlearn/emlearn
- **License:** MIT (`upstream/LICENSE.md`) — permissive; preserved.
- **Baseline pinned:** `578d89dcd97e3eb47f993571b9854fb6c22a2f73`
  (17 Jul 2026). Vendored as git submodule at `upstream/`, zero files modified.

## What existed before my contribution
Converters for trees/forests, MLP, kNN, Naive Bayes, mixture models;
`cgen.py` code-gen helpers; `common.CompiledClassifier` host parity harness;
Arduino/Zephyr examples; C runtime headers `eml_*.h`. No linear-model
converter (upstream issue #56), no ESP32+DHT deployment example.

## What I changed (P2)
- ADDED `python/emlearn_linear/linear.py` (mine, mirrors `trees.Wrapper` API)
- ADDED `tests/test_linear_parity.py`, `firmware/`, `examples/`, `tools/` (mine)
- MODIFIED upstream files: **none**.
