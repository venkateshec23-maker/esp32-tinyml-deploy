# esp32-tinyml-deploy

Linear-model TinyML for microcontrollers: a tested sklearn→C converter for
logistic/linear regression (closing upstream emlearn issue #56) plus a real
ESP32 DevKit deployment — DHT comfort classifier with measured
flash/RAM/latency.

> **Status (host-complete 2026-10-07):** 8/8 parity tests green; classifier
> firmware builds (+228 B flash); host benchmark + rule-grid model card in
> `reports/`. **No on-device run — no kit available** (see
> `docs/limitations.md` for the exact pending procedure).

## Upstream & attribution
Core framework: [emlearn/emlearn](https://github.com/emlearn/emlearn) (MIT),
vendored as a pinned submodule (`upstream/`, untouched). My converter mirrors
their `trees.Wrapper` API. See `docs/attribution.md`.

## Layout
`python/emlearn_linear/` (my converter) · `firmware/` (ESP32 sketch) ·
`examples/sensor_dataset/` (data + training) · `tests/` (parity) ·
`reports/` (evidence) · `docs/`
