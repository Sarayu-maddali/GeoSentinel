from datetime import datetime, timezone


DEMO_PROVENANCE = {
    "DEMO_SCENE_001": {
        "scene_id": "DEMO_SCENE_001",
        "product_id": "DEMO_PRODUCT_001",
        "source": "LOCAL DEMONSTRATION DATA",
        "satellite": "Sentinel-2",
        "sensor": "MSI",
        "acquisition_date": "2025-01-12",
        "resolution_m": 10,
        "processing": [
            "cloud_mask",
            "normalization",
            "tiling"
        ],
        "quality_control": {
            "cloud": "PASS",
            "haze": "PASS",
            "registration": "PASS"
        },
        "embedding_model": "DEMO_EMBEDDING_MODEL",
        "change_model": "DEMO_CHANGE_MODEL",
        "index_version": "DEMO_INDEX_V1",
        "processing_version": "DEMO_PIPELINE_V1",
        "analysis_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "is_demo": True
    }
}


def get_provenance(scene_id: str):

    return DEMO_PROVENANCE.get(scene_id)