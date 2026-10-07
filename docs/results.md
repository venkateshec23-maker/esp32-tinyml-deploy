# Results (measured 2026-10-07, host; on-device pending hardware)

## Converter parity (TDM-GCC -O2, `-Wall -Wextra -Werror`, fixed seeds)
- 8/8 pytest green: binary + 3-class + single-feature + nonstandard labels
  predict parity EXACT; proba max-abs-err < 1e-5; regression < 1e-4.
- Generated C has no Python deps (asserted in test).

## Model (rule-grid fallback, SOURCE recorded in model_card.json)
- 3-class multinomial logistic on [T, RH]; train accuracy **0.8767**
  (linear boundaries can't fully separate the rule's corners — expected,
  documented, interview-relevant).
- `model.h`: **1346 bytes**.

## Firmware (arduino-cli 1.2.2, esp32 core 3.3.11, DHT 1.4.7)
- LOG_RAW build: 274,244 B flash (20%), 22,140 B RAM (6%).
- Classifier build (baked model.h, LOG_RAW=0): 274,472 B flash.
- **Whole classifier costs +228 B flash, +0 B RAM.**

## Latency
- Host: below measurement floor (see bench_host.json) — reported as a bound,
  not a number. ESP32 `micros()` per-inference + heap readings are implemented
  in the sketch and pending hardware.

## What was NOT measured (no hardware)
No flash test, no serial log, no on-device parity. `docs/limitations.md` holds
the exact pending procedure so a future run (with kit) is one session's work.
