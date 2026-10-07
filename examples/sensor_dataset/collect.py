"""collect.py — log raw DHT CSV lines from serial into dataset.csv.

Usage: python collect.py --port COM7 --baud 115200 --out dataset.csv --seconds 600
Validates each line (2 floats, sane ranges) and reports reject counts, so a
miswired sensor or wrong DHT type shows up HERE, not silently in training.
"""

import argparse
import csv
import sys
import time

try:
    import serial
except ImportError:
    sys.exit('pyserial missing: pip install pyserial')


def valid(t, h):
    return -40.0 <= t <= 80.0 and 0.0 <= h <= 100.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--port', required=True)
    ap.add_argument('--baud', type=int, default=115200)
    ap.add_argument('--out', default='dataset.csv')
    ap.add_argument('--seconds', type=int, default=600)
    args = ap.parse_args()

    ser = serial.Serial(args.port, args.baud, timeout=2)
    deadline = time.time() + args.seconds
    kept = rejected = 0
    with open(args.out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['temp_c', 'rh_pct'])
        while time.time() < deadline:
            line = ser.readline().decode('utf-8', 'replace').strip()
            if not line or line.startswith('#'):
                continue
            try:
                t, h = (float(v) for v in line.split(',')[:2])
            except ValueError:
                rejected += 1
                continue
            if not valid(t, h):
                rejected += 1
                continue
            w.writerow([f'{t:.2f}', f'{h:.2f}'])
            kept += 1
    print(f'kept={kept} rejected={rejected} -> {args.out}')


if __name__ == '__main__':
    main()
