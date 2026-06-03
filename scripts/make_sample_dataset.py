#!/usr/bin/env python3
"""Create a small synthetic EMG CSV for repository smoke tests."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


LABEL_TO_ACTION = {
    0: "fist",
    1: "relax",
    2: "open",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a synthetic EMG gesture dataset.")
    parser.add_argument("--output", type=Path, default=Path("emg_hand_gestures.csv"))
    parser.add_argument("--samples-per-class", type=int, default=32)
    parser.add_argument("--length", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def make_signal(label: int, length: int, rng: np.random.Generator) -> np.ndarray:
    t = np.linspace(0.0, 1.0, length, dtype=np.float32)

    if label == 0:
        envelope = 0.35 + 0.65 * np.sin(np.pi * t) ** 2
        base = 0.75 * np.sin(2 * np.pi * 18 * t) + 0.25 * np.sin(2 * np.pi * 42 * t)
    elif label == 1:
        envelope = np.full_like(t, 0.2)
        base = 0.18 * np.sin(2 * np.pi * 9 * t)
    else:
        envelope = 0.25 + 0.55 * (1.0 - np.cos(2 * np.pi * t)) / 2.0
        base = 0.55 * np.sin(2 * np.pi * 13 * t + 0.7) + 0.2 * np.sin(2 * np.pi * 31 * t)

    noise = rng.normal(0.0, 0.06, size=length)
    drift = rng.normal(0.0, 0.015) * np.linspace(-1.0, 1.0, length)
    return (envelope * base + noise + drift).astype(np.float32)


def main() -> None:
    args = parse_args()
    if args.samples_per_class < 3:
        raise ValueError("--samples-per-class must be at least 3.")
    if args.length <= 0:
        raise ValueError("--length must be positive.")

    rng = np.random.default_rng(args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [f"signal_{index}" for index in range(args.length)] + ["label", "action"]
    with args.output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for label, action in LABEL_TO_ACTION.items():
            for _ in range(args.samples_per_class):
                signal = make_signal(label=label, length=args.length, rng=rng)
                row = {f"signal_{index}": f"{value:.6f}" for index, value in enumerate(signal)}
                row["label"] = label
                row["action"] = action
                writer.writerow(row)

    print(f"wrote {args.output} ({args.samples_per_class * len(LABEL_TO_ACTION)} rows)")


if __name__ == "__main__":
    main()
