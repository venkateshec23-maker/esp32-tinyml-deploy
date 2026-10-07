# Limitations (P2 host-complete — honest boundary)

- **No on-device run: no ESP32/DHT kit available.** The sketch compiles for
  `esp32:esp32:esp32` and implements latency/heap reporting, but no flash,
  serial, or on-device parity evidence exists. Pending procedure: flash
  LOG_RAW build → `collect.py --port COMx` (10+ min varied conditions) →
  `label_train.py` (no `--allow-rule-grid`) → `bake_model.py` → rebuild with
  `-DLOG_RAW=0` → flash → capture serial → compare vs sklearn.
- `model_card.json` in the training run says `source: rule-grid` — any claim
  citing the model must cite this field.
- Float only; no fixed-point (upstream #77 is the horizon).
- Windows host parity uses TDM-GCC directly (setuptools needs MSVC); the
  library keeps the upstream `CompiledClassifier` path for other platforms.
- Tested on Vivado-free host; no interaction with P1 repo.
