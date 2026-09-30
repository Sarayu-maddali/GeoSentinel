from datetime import date
from typing import Any


DEMO_SCENES = [
    {
        "id": "DEMO_SCENE_001",
        "satellite": "Sentinel-2",
        "sensor": "MSI",
        "date": "2025-01-12",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "cloud_cover": 5,
        "resolution": 10,
        "quality_score": 0.94,
        "semantic_score": 0.91,
        "thumbnail_url": None,
        "is_demo": True
    },
    {
        "id": "DEMO_SCENE_002",
        "satellite": "Sentinel-1",
        "sensor": "SAR",
        "date": "2025-01-14",
        "latitude": 12.9352,
        "longitude": 77.6245,
        "cloud_cover": None,
        "resolution": 10,
        "quality_score": 0.89,
        "semantic_score": 0.87,
        "thumbnail_url": None,
        "is_demo": True
    },
    {
        "id": "DEMO_SCENE_003",
        "satellite": "Landsat-9",
        "sensor": "OLI/TIRS",
        "date": "2025-01-16",
        "latitude": 13.0827,
        "longitude": 77.5877,
        "cloud_cover": 8,
        "resolution": 30,
        "quality_score": 0.86,
        "semantic_score": 0.82,
        "thumbnail_url": None,
        "is_demo": True
    }
]


def _normalise(value: float) -> float:
    return max(0.0, min(1.0, value))


def calculate_ranking_score(scene: dict[str, Any]) -> float:

    semantic = _normalise(
        scene.get("semantic_score", 0)
    )

    spatial = _normalise(
        scene.get("spatial_score", 0.8)
    )

    temporal = _normalise(
        scene.get("temporal_score", 0.8)
    )

    quality = _normalise(
        scene.get("quality_score", 0)
    )

    resolution = _normalise(
        1 / max(scene.get("resolution", 30), 1)
        * 10
    )

    return (
        0.50 * semantic
        + 0.20 * spatial
        + 0.15 * temporal
        + 0.10 * quality
        + 0.05 * resolution
    )


def _date_in_range(scene_date: str, start_date: str | None, end_date: str | None) -> bool:
    current = date.fromisoformat(scene_date)
    return (not start_date or current >= date.fromisoformat(start_date)) and (
        not end_date or current <= date.fromisoformat(end_date)
    )


def unified_search(
    query: str | None = None,
    bbox: list[float] | None = None,
    satellites: list[str] | None = None,
    cloud_cover: float | None = None,
    start_date: str | None = None,
    end_date: str | None = None
):

    results = [scene.copy() for scene in DEMO_SCENES]

    if start_date and end_date and date.fromisoformat(start_date) > date.fromisoformat(end_date):
        raise ValueError("start_date must be before or equal to end_date")

    if query and not query.strip():
        raise ValueError("query cannot be empty")

    if satellites:
        allowed = {
            satellite.lower()
            for satellite in satellites
        }

        results = [
            scene
            for scene in results
            if scene["satellite"].lower()
            in allowed
        ]

    if cloud_cover is not None:
        results = [
            scene
            for scene in results
            if scene["cloud_cover"] is None
            or scene["cloud_cover"] <= cloud_cover
        ]

    if bbox:
        min_lon, min_lat, max_lon, max_lat = bbox
        results = [
            scene for scene in results
            if min_lat <= scene["latitude"] <= max_lat
            and min_lon <= scene["longitude"] <= max_lon
        ]

    if start_date or end_date:
        results = [
            scene for scene in results
            if _date_in_range(scene["date"], start_date, end_date)
        ]

    for scene in results:
        scene["ranking_components"] = {
            "semantic": scene["semantic_score"],
            "spatial": scene.get("spatial_score", 0.8),
            "temporal": scene.get("temporal_score", 0.8),
            "quality": scene["quality_score"],
            "resolution": round(1 / max(scene.get("resolution", 30), 1) * 10, 4),
        }
        scene["ranking_score"] = round(calculate_ranking_score(scene), 4)

    results.sort(
        key=lambda scene: scene["ranking_score"],
        reverse=True
    )

    return {
        "query": query,
        "count": len(results),
        "results": results,
        "pipeline": [
            "natural_language_query",
            "semantic_retrieval_demo_fallback",
            "metadata_filtering",
            "spatial_filtering",
            "temporal_filtering",
            "quality_filtering",
            "ranking",
            "top_k",
        ],
        "filters_applied": {
            "bbox": bbox,
            "start_date": start_date,
            "end_date": end_date,
            "satellites": satellites,
            "cloud_cover": cloud_cover,
        },
        "semantic_source": "demo_fallback",
        "is_demo": True
    }