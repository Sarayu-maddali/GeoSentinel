"""Raster ingestion and deterministic preprocessing for the development index.

This module intentionally does not generate embeddings or mutate the FAISS index.
Those concerns belong to later phases. It prepares one source raster at a time,
preserving geospatial metadata and producing a stable normalized array for the
future embedding service.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


SUPPORTED_EXTENSIONS = {".tif", ".tiff", ".jp2", ".png", ".jpg", ".jpeg"}
DEFAULT_RAW_DIR = Path(__file__).resolve().parents[3] / "data" / "raw"
DEFAULT_PROCESSED_DIR = Path(__file__).resolve().parents[3] / "data" / "processed"


class IngestionError(ValueError):
    """Raised when a source raster cannot be safely prepared."""


@dataclass(frozen=True)
class RasterMetadata:
    scene_id: str
    source_path: str
    source_format: str
    width: int
    height: int
    band_count: int
    dtype: str
    crs: str | None = None
    bbox: list[float] | None = None
    transform: list[float] | None = None
    acquisition_datetime: str | None = None
    satellite: str | None = None
    sensor: str | None = None
    cloud_cover: float | None = None
    source_sha256: str | None = None
    preprocessing: str = "band-wise finite-value min-max normalization"


def _safe_scene_id(path: Path) -> str:
    """Use a filesystem-safe stable identifier derived from the source name."""
    stem = "".join(character if character.isalnum() or character in "-_" else "_" for character in path.stem)
    digest = hashlib.sha256(str(path.resolve()).encode("utf-8")).hexdigest()[:12]
    return f"{stem[:80] or 'scene'}-{digest}"


def _source_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _finite_range(band: np.ndarray) -> tuple[float, float]:
    finite = band[np.isfinite(band)]
    if finite.size == 0:
        return 0.0, 1.0
    low = float(finite.min())
    high = float(finite.max())
    return low, high if high > low else low + 1.0


def preprocess_array(array: np.ndarray, target_size: tuple[int, int] | None = None) -> np.ndarray:
    """Return channels-first float32 data normalized independently per band.

    No fabricated pixels are added. Optional resizing uses nearest-neighbour
    sampling and is deterministic, which keeps later embedding comparisons
    reproducible across ingestion runs.
    """
    values = np.asarray(array)
    if values.ndim == 2:
        values = values[np.newaxis, ...]
    if values.ndim != 3:
        raise IngestionError("raster data must have shape (bands, height, width)")
    if values.shape[0] == 0 or values.shape[1] == 0 or values.shape[2] == 0:
        raise IngestionError("raster data cannot contain an empty dimension")

    normalized = np.empty(values.shape, dtype=np.float32)
    for band_index, band in enumerate(values.astype(np.float32, copy=False)):
        low, high = _finite_range(band)
        safe_band = np.nan_to_num(band, nan=low, posinf=high, neginf=low)
        normalized[band_index] = np.clip((safe_band - low) / (high - low), 0.0, 1.0)

    if target_size is None or target_size == normalized.shape[1:]:
        return normalized
    target_height, target_width = target_size
    if target_height < 1 or target_width < 1:
        raise IngestionError("target_size must contain positive dimensions")
    row_indices = np.linspace(0, normalized.shape[1] - 1, target_height).round().astype(int)
    col_indices = np.linspace(0, normalized.shape[2] - 1, target_width).round().astype(int)
    return normalized[:, row_indices][:, :, col_indices]


def _read_raster(path: Path) -> tuple[np.ndarray, dict[str, Any]]:
    if path.suffix.lower() in {".tif", ".tiff", ".jp2"}:
        try:
            import rasterio
        except ImportError as error:
            raise IngestionError("GeoTIFF/JP2 ingestion requires the declared rasterio dependency") from error
        with rasterio.open(path) as dataset:
            array = dataset.read()
            bounds = dataset.bounds
            metadata = {
                "crs": str(dataset.crs) if dataset.crs else None,
                "bbox": [bounds.left, bounds.bottom, bounds.right, bounds.top],
                "transform": list(dataset.transform),
                "width": dataset.width,
                "height": dataset.height,
                "band_count": dataset.count,
                "dtype": str(dataset.dtypes[0]),
            }
            return array, metadata

    try:
        from PIL import Image
    except ImportError as error:
        raise IngestionError("PNG/JPEG ingestion requires the declared Pillow dependency") from error
    with Image.open(path) as image:
        array = np.asarray(image)
    if array.ndim == 2:
        array = array[np.newaxis, ...]
    else:
        array = np.moveaxis(array, -1, 0)
    return array, {
        "crs": None,
        "bbox": None,
        "transform": None,
        "width": array.shape[2],
        "height": array.shape[1],
        "band_count": array.shape[0],
        "dtype": str(array.dtype),
    }


def ingest_raster(
    source_path: str | Path,
    processed_dir: str | Path = DEFAULT_PROCESSED_DIR,
    *,
    target_size: tuple[int, int] | None = (224, 224),
    metadata: dict[str, Any] | None = None,
) -> RasterMetadata:
    """Prepare one raster and write its normalized array plus metadata sidecar.

    Existing outputs are reused when their source hash matches, enabling
    incremental ingestion without rebuilding already-prepared scenes.
    """
    source = Path(source_path).expanduser().resolve()
    if not source.is_file():
        raise IngestionError(f"source image does not exist: {source}")
    if source.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise IngestionError(f"unsupported raster extension: {source.suffix or '<none>'}")

    output_dir = Path(processed_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    scene_id = _safe_scene_id(source)
    output_array = output_dir / f"{scene_id}.npy"
    output_metadata = output_dir / f"{scene_id}.json"
    source_hash = _source_sha256(source)

    if output_array.exists() and output_metadata.exists():
        cached = json.loads(output_metadata.read_text(encoding="utf-8"))
        if cached.get("source_sha256") == source_hash:
            return RasterMetadata(**cached)

    array, raster_info = _read_raster(source)
    processed = preprocess_array(array, target_size=target_size)
    np.save(output_array, processed, allow_pickle=False)
    supplied = metadata or {}
    record = RasterMetadata(
        scene_id=scene_id,
        source_path=str(source),
        source_format=source.suffix.lower().lstrip("."),
        source_sha256=source_hash,
        acquisition_datetime=supplied.get("acquisition_datetime"),
        satellite=supplied.get("satellite"),
        sensor=supplied.get("sensor"),
        cloud_cover=supplied.get("cloud_cover"),
        **raster_info,
    )
    output_metadata.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")
    return record


def ingest_directory(
    raw_dir: str | Path = DEFAULT_RAW_DIR,
    processed_dir: str | Path = DEFAULT_PROCESSED_DIR,
    *,
    target_size: tuple[int, int] | None = (224, 224),
) -> list[RasterMetadata]:
    """Ingest supported files from a directory, skipping unchanged outputs."""
    source_dir = Path(raw_dir).expanduser().resolve()
    if not source_dir.is_dir():
        raise IngestionError(f"raw directory does not exist: {source_dir}")
    Path(processed_dir).expanduser().resolve().mkdir(parents=True, exist_ok=True)
    records = []
    for source in sorted(source_dir.iterdir()):
        if source.is_file() and source.suffix.lower() in SUPPORTED_EXTENSIONS:
            records.append(ingest_raster(source, processed_dir, target_size=target_size))
    return records
