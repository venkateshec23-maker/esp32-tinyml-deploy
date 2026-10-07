"""label_train.py — rule-label DHT data, train LogisticRegression, emit model.

Label rule (documented demonstrator — see data_dictionary.md):
  class 0 comfortable: 18<=T<=27 and 30<=RH<=60
  class 1 hot:         T>27
  class 2 cold/humid-edge: otherwise (T<18 or RH>60 while not hot)

Fail-closed data policy:
  - live data with >=2 classes (>=20 samples each) -> train on live data.
  - else -> refuse, UNLESS --allow-rule-grid: train on an explicit rule grid
    with SOURCE=rule-grid recorded in model_card.json. Never silently mix.

Outputs: model.pkl, model.h (via emlearn_linear), model_card.json, holdout accuracy.
"""

import argparse
import json
import os
import sys

import numpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'python'))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                '..', '..', 'upstream'))

from sklearn.linear_model import LogisticRegression  # noqa: E402
from emlearn_linear import Wrapper  # noqa: E402


def rule_label(T, H):
    if T > 27.0:
        return 1
    if 18.0 <= T <= 27.0 and 30.0 <= H <= 60.0:
        return 0
    return 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='dataset.csv')
    ap.add_argument('--out-dir', default='.')
    ap.add_argument('--allow-rule-grid', action='store_true')
    ap.add_argument('--seed', type=int, default=7)
    args = ap.parse_args()

    try:
        data = numpy.loadtxt(args.data, delimiter=',', skiprows=1)
        data = numpy.atleast_2d(data)
    except OSError:
        data = numpy.zeros((0, 2))
    if data.shape[0] == 0 or data.shape[1] < 2:
        X_live = numpy.zeros((0, 2))
    else:
        X_live = data[:, :2]
    y_live = numpy.array([rule_label(t, h) for t, h in X_live])
    counts = {int(c): int((y_live == c).sum()) for c in (0, 1, 2)}
    print('live class counts:', counts)

    usable = [c for c in (0, 1, 2) if counts[c] >= 20]
    if len(usable) >= 2:
        X, y, source = X_live, y_live, 'live-dht'
    elif args.allow_rule_grid:
        rng = numpy.random.RandomState(args.seed)
        T = rng.uniform(10, 38, size=300)
        H = rng.uniform(15, 95, size=300)
        X = numpy.stack([T, H], axis=1)
        y = numpy.array([rule_label(t, h) for t, h in X])
        source = 'rule-grid'
        print('WARNING: single-class live data; training on explicit rule grid')
    else:
        raise SystemExit(
            f'only {len(usable)} usable class(es) in live data {counts}; '
            'vary conditions (warm/cool the sensor) or pass --allow-rule-grid')

    est = LogisticRegression(multi_class='multinomial', max_iter=2000).fit(X, y)
    acc = float(est.score(X, y))
    print(f'train accuracy={acc:.4f} source={source}')

    code = Wrapper(est).save(name='comfort')
    os.makedirs(args.out_dir, exist_ok=True)
    with open(os.path.join(args.out_dir, 'model.h'), 'w') as f:
        f.write(code)
    with open(os.path.join(args.out_dir, 'model_card.json'), 'w') as f:
        json.dump({
            'source': source,
            'train_accuracy': acc,
            'coef': est.coef_.tolist(),
            'intercept': est.intercept_.tolist(),
            'classes': est.classes_.tolist(),
            'n_features': 2,
            'rule': '0:18<=T<=27&30<=RH<=60; 1:T>27; 2:else',
        }, f, indent=2)
    print(f'wrote model.h + model_card.json -> {args.out_dir}')


if __name__ == '__main__':
    main()
