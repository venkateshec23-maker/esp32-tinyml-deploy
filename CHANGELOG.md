# Changelog — esp32-tinyml-deploy
## [0.1.0] — 2026-10-07 — host-complete (no kit: on-device pending)
### Added
- `python/emlearn_linear/linear.py` — Logistic/LinearRegression → C (8 tests green)
- ESP32 sketch (LOG_RAW + classifier modes), dataset tooling, bake + bench tools
- rule-grid model (acc 0.8767, SOURCE recorded), firmware sizes, host bench bound
### Deferred (needs hardware)
- flash, live-data collection, on-device parity + latency (procedure documented)
