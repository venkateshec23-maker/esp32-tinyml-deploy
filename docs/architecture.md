# P2 Architecture — esp32-tinyml-deploy

## Layout
```
esp32-tinyml-deploy/
├── upstream/                  # emlearn submodule, pinned 578d89d (READ-ONLY)
├── python/emlearn_linear/
│   ├── linear.py              # MY converter: Wrapper + inline C generation
│   └── __init__.py
├── firmware/esp32_sensor_clf/ # MY Arduino sketch (DHT → predict → serial/LED)
├── examples/sensor_dataset/   # MY collect.py + label_train.py + data dictionary
├── tests/test_linear_parity.py # MY sklearn-vs-C parity tests (fixed seeds)
├── tools/                     # MY build/flash/monitor helpers (+arduino-cli pin)
├── reports/                   # generated: parity logs, build sizes, device logs
└── docs/
```

## Data flow
```
collect.py (serial DHT log) → dataset.csv → label_train.py (rule + sklearn)
  → weights baked into sketch via linear.py save() → arduino-cli build
  → flash → device prints predictions + latency → reports/device_log.txt
  → parity check vs sklearn → docs/results.md
```

## Interfaces
- `linear.Wrapper(estimator, method='inline').save(name)` → C source string
  with `<name>_predict(const float *f, int32_t n)` (+ `_predict_proba` for
  classifiers). Same naming/shape convention as upstream `trees.Wrapper`.
- Sketch ↔ model: single generated header pasted into sketch dir at build
  time by `tools/bake_model.py` (keeps generated artifact out of git).
- Honesty interface: every number in results.md names its instrument
  (build log / micros() / heap API) — estimates are labeled EST, never shipped.
