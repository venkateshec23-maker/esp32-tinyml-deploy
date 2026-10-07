# P2 Requirements — linear models for emlearn + ESP32 deployment

## 1. Goal
Close upstream `emlearn/emlearn` issue #56 (no linear-model support) with a
tested converter, and prove it on real hardware: a DHT-based comfort
classifier deployed on a plain ESP32 DevKit with measured flash/RAM/latency.

## 2. Background
emlearn converts sklearn models to C for microcontrollers (trees, MLP,
kNN, Bayes exist). Linear models — the cheapest classifiers that fit any MCU —
are missing (open issue #56). Linear inference is a dot product + bias:
~10 lines of C, exactly verifiable against sklearn, near-zero flash.

## 3. Scope (P2)
- `python/emlearn_linear/linear.py`: `Wrapper` mirroring upstream `trees.py`
  convention — supports `LogisticRegression` (binary + multinomial/one-vs-rest)
  and `LinearRegression`; inline C generation (`<name>_predict`, optional
  `<name>_predict_proba`); `save()` returning C source; `predict()` parity via
  upstream `common.CompiledClassifier` (host gcc).
- `tests/test_linear_parity.py`: C-vs-sklearn agreement on fixed-seed
  datasets (binary, 3-class, regression); edge cases (single feature,
  TIMESTAMPS n/a).
- `firmware/esp32_sensor_clf/`: Arduino sketch for ESP32 DevKit + DHT
  (select pin at build time): reads T/RH → feature vector → generated
  `comfort_predict()` → Serial output + on-board LED state. Reports
  `micros()` inference latency and `ESP.getFreeHeap()`.
- `examples/sensor_dataset/`: data-collection sketch + labeling script
  (rule-labeled comfort zones — documented as demonstrator, not discovery)
  + training script producing the deployed weights.
- Benchmark table in `docs/results.md`: sklearn-vs-C agreement (must be 100%
  on test vectors within float tolerance), flash bytes (from build log),
  heap delta, mean/p99 inference latency on-device.

## 4. Non-goals
- No SVM/PCA (issues #55/#57 — separate contributions).
- Float first; no fixed-point in P2 (documented; upstream #77 is the horizon).
- No edits inside `upstream/` (pinned `578d89d`).
- No claim the comfort classes are a discovered phenomenon: labels come from
  a documented rule; the contribution is the *conversion + deployment
  pipeline with measurements*, stated as such everywhere.

## 5. Acceptance criteria
1. `pytest tests/` green: parity 100% on all fixed-seed vectors.
2. Generated C has no sklearn/numpy dependency (pure C + stdint).
3. Sketch compiles for `esp32:esp32:esp32` via reproducible CLI build.
4. On-device predictions on logged vectors match sklearn exactly.
5. `docs/results.md` holds measured (not estimated) flash/RAM/latency.
6. Upstream issue #56 referenced; no upstream file modified.

## 6. Environment
Win10, Python 3.12, sklearn 1.4.2, TDM-GCC (host parity compile),
ESP32 Arduino core 3.3.11, plain ESP32 DevKit + DHT sensor on a selectable pin.
arduino-cli: pinned into `tools/` if needed for headless builds.

## 7. Risks
- DHT timing on ESP32 core 3.x (DHT lib compatibility — verify by reading,
  not assuming; fallback: analog dummy sensor with documented substitution).
- Arduino DHT library version drift — pin versions in docs.
- Float on ESP32 is fast enough that latency may be sub-microsecond noise —
  report distribution + measurement method, not a single number.
