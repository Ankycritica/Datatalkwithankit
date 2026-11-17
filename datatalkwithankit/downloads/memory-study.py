"""Reproduce the site's memory-capacity estimates using only Python's standard library.

These are calculated planning scenarios, not measurements of serving performance.
Usage: python3 memory-study.py --config memory-study-config.json --output results.csv
Memory units are decimal GB. Rates are a dated snapshot, not current rental quotes.
"""
import argparse
import csv
from decimal import Decimal, ROUND_CEILING
import json
from pathlib import Path
import sys


FIELDS = [
    "model_billions", "precision", "weights_gb", "headroom_gb", "total_gb",
    "gpu", "gpu_memory_gb", "gpus", "price_per_gpu_hour",
    "estimated_hourly_usd", "price_date",
]


def scenarios(config):
    """Yield the full, deterministic model × precision × GPU matrix."""
    margin = Decimal(str(config["headroom_fraction"]))
    for size in config["model_billions"]:
        for precision, byte_count in config["bytes_per_parameter"].items():
            weights = Decimal(str(size)) * Decimal(str(byte_count))
            headroom = weights * margin
            total = weights + headroom
            for gpu in config["gpus"]:
                minimum = int((total / Decimal(str(gpu["memory_gb"]))).to_integral_value(rounding=ROUND_CEILING))
                count = 1
                while count < minimum:
                    count *= 2
                rate = Decimal(str(gpu["hourly_usd"]))
                yield dict(zip(FIELDS, [
                    size, precision, str(weights), str(headroom), str(total),
                    gpu["name"], gpu["memory_gb"], count, format(rate, ".2f"),
                    format(rate * count, ".2f"), config["price_date"],
                ]))


def write_results(config, stream):
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(scenarios(config))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("memory-study-config.json"))
    parser.add_argument("--output", type=Path, help="Write CSV to this file; otherwise write to stdout.")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if args.output:
        with args.output.open("w", newline="", encoding="utf-8") as stream:
            write_results(config, stream)
    else:
        write_results(config, sys.stdout)


if __name__ == "__main__":
    main()
