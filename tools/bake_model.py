"""bake_model.py — copy a trained model.h into the sketch dir (generated, gitignored).

Usage: python bake_model.py --model-h <path> [--sketch-dir <path>]
Prints weight summary for the engineering record. Refuses to bake if the
model has != 2 features (this sketch feeds [T, RH]).
"""

import argparse
import json
import os
import shutil
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model-h', required=True)
    ap.add_argument('--sketch-dir', default=None)
    ap.add_argument('--model-card', default=None)
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sketch = args.sketch_dir or os.path.join(root, 'firmware', 'esp32_sensor_clf')
    dst = os.path.join(sketch, 'model.h')
    shutil.copyfile(args.model_h, dst)
    print(f'baked -> {dst}')

    card = args.model_card or os.path.join(os.path.dirname(args.model_h), 'model_card.json')
    if os.path.exists(card):
        info = json.load(open(card))
        print('source:', info.get('source'), '| train_acc:', info.get('train_accuracy'))
        if info.get('n_features') != 2:
            sys.exit('refusing: sketch needs exactly 2 features [T, RH]')


if __name__ == '__main__':
    main()
