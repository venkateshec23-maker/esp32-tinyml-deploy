# Testing (P2 host-complete)

## Executed (2026-10-07, all green)
- `pytest tests/`: 8/8 — parity exact on classes, proba <1e-5, regression
  <1e-4; rejection tests (unfitted/unsupported); C-purity assertion.
- Generated C compiles under `gcc -std=c99 -Wall -Wextra -Werror -O2`
  (the harness; warnings fail the suite — caught 2 real issues).
- `label_train.py --allow-rule-grid`: accuracy 0.8767, artifacts emitted.
- `bake_model.py` + classifier-mode firmware compile (sizes in results.md).

## Failures observed and fixed (evidence tests discriminate)
1. `lin_logit` unused-parameter under `-Werror` → generator now emits
   `(void)features_length`.
2. Harness `out[]` maybe-uninitialized under `-Werror` → zero-init in harness
   (not in model under test).
3. My `argmax(axis=1)` fixture bug → caught by sklearn validation, fixed.
4. `bake_model.py` wrong repo-root depth → fixed, verified by successful bake.
5. Host latency harness produced untrustworthy ns (0.0, then 1.8ns) →
   methodology corrected to report bound + wall time, not fake precision.

## Not executed (no hardware)
On-device flash, serial parity, ESP32 latency/heap capture.
