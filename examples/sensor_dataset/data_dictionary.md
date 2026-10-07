# Data dictionary — DHT comfort demonstrator

## Sensor
DHT22 (or DHT11 — set `DHT_TYPE` in sketch) on pin 15 (override `DHT_PIN`).
2 s sampling. `collect.py` rejects non-numeric lines and out-of-range
values (T in [-40, 80] °C, RH in [0, 100] %); reject counts are printed.

## Columns (`dataset.csv`)
`temp_c` (float, °C), `rh_pct` (float, %RH). No timestamps (order = time).

## Labels (rule — NOT a discovered phenomenon)
- `0 comfortable`: 18<=T<=27 AND 30<=RH<=60
- `1 hot`: T>27
- `2 cold-or-humid edge`: anything else

## Provenance
`model_card.json` records `source`: `live-dht` (trained on collected rows)
or `rule-grid` (explicit fallback when live data is single-class).
Any result citing the model must cite the source field.
