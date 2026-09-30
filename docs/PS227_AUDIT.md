# SIH26227 Audit and Phase 2 Boundary

## 1. Existing architecture

- FastAPI application entry point: `backend/app/main.py`.
- Routes are separated under `backend/app/routes/` and delegate to services under `backend/app/services/`.
- Existing STAC discovery is in `stac_service.py` and uses `pystac-client` against the Copernicus STAC URL.
- The frontend is React + Vite with Leaflet and Axios. API calls are centralized in `frontend/src/api.js`.
- `DATABASE_URL` is configured, but no SQLAlchemy/PostGIS models, sessions, migrations, or database reads/writes are currently used.

## 2. Existing working features

- `GET /api/search` calls the existing Sentinel-2 STAC service with bbox, date range, cloud cover, and limit.
- FastAPI route registration, CORS, health, review persistence, and the Person 3 UI workflow are present.
- Review decisions are persisted to `backend/app/data/reviews.json` with an audit list.

## 3. Demo/mock features

- `backend/app/services/unified_search.py` reads only `DEMO_SCENES`; semantic, quality, spatial, temporal, and resolution values are manually supplied.
- The unified pipeline label includes `semantic_retrieval_demo_fallback`; it does not call an embedding model or vector index.
- Temporal analysis returns a demo no-change result when no detector is supplied.
- Clustering and provenance are static demo dictionaries.
- The frontend displays explicit DEMO badges and unavailable-image states, but it currently has no upload flow.

## 4. Missing PS227 requirements

- Raster upload validation and storage endpoint.
- Real image preprocessing and geospatial metadata ingestion.
- Embedding model initialization and image/text embedding.
- Persistent FAISS/vector index and vector-to-metadata mapping.
- Image-to-image and text-to-image semantic retrieval.
- STAC asset download/preview integration.
- Real change detector and quality-aware confidence.
- Embedding-based clustering.
- Evaluation datasets, held-out retrieval judgments, and change-detection metrics.

## 5. Reusable dependencies

`requirements.txt` already declares `rasterio`, `numpy`, `Pillow`, OpenCV, PyTorch, Transformers, Sentence Transformers, FAISS, scikit-learn, SciPy, STAC, and database libraries. In the active interpreter, only NumPy and `pystac-client` were importable; the repository virtual environment points to a missing Python executable. No package was installed during this phase.

## 6. Storage and database findings

The repository has empty `data/raw`, `data/processed`, `data/embeddings`, `data/results`, and `data/tiles` directories. `models/` is empty. The current service stores only review JSON; large imagery is not stored in a database.

## 7. Phase 2 implementation

`backend/app/services/ingestion_service.py` now provides:

- extension and file existence validation;
- stable, filesystem-safe scene IDs;
- SHA-256 source tracking for incremental reuse;
- channels-first `float32` band-wise finite-value min-max normalization;
- deterministic optional resizing;
- lazy GeoTIFF/JP2 support through rasterio;
- lazy PNG/JPEG support through Pillow;
- raster CRS, bounds, transform, dimensions, band count, and dtype capture;
- normalized `.npy` output and JSON metadata sidecars under `data/processed`;
- directory ingestion that skips unchanged files.

The CLI is `scripts/ingest_imagery.py`. It does not download data, create embeddings, or alter the existing API routes.

## 8. Recommended next phases

1. Verify the Python environment and install only the already-declared dependencies needed for the selected local embedding model.
2. Add a model adapter with explicit model/version metadata and deterministic image/text embedding methods.
3. Add persistent FAISS index plus metadata mapping and incremental append behavior.
4. Add upload and ingestion APIs with bounded file size, MIME/extension checks, safe storage, and sanitized client metadata.
5. Replace unified demo retrieval with vector retrieval while preserving existing STAC search.
6. Integrate STAC assets and real previews, then implement real temporal and quality-aware analysis.
7. Add clustering, evaluation artifacts, and end-to-end frontend upload/search flows.
