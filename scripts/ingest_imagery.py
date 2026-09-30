"""Prepare local development imagery for later embedding/indexing phases.

Usage from the repository root:
    python scripts/ingest_imagery.py --raw-dir data/raw --processed-dir data/processed

This command does not download data and does not create embeddings. Place a
small, licensed development subset in data/raw first.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.services.ingestion_service import IngestionError, ingest_directory


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare satellite rasters for indexing")
    parser.add_argument("--raw-dir", default="data/raw")
    parser.add_argument("--processed-dir", default="data/processed")
    parser.add_argument("--size", type=int, default=224, help="square output size in pixels")
    args = parser.parse_args()

    if args.size < 1:
        parser.error("--size must be positive")
    try:
        records = ingest_directory(args.raw_dir, args.processed_dir, target_size=(args.size, args.size))
    except IngestionError as error:
        parser.error(str(error))
    print(json.dumps([record.__dict__ for record in records], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
