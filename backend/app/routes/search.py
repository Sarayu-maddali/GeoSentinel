from fastapi import APIRouter, Query

from app.services.stac_service import search_sentinel2


router = APIRouter()


@router.get("/search")
def search_images(
    min_lon: float = Query(...),
    min_lat: float = Query(...),
    max_lon: float = Query(...),
    max_lat: float = Query(...),

    start_date: str = Query(...),
    end_date: str = Query(...),

    cloud_cover: float = Query(30),
    limit: int = Query(20)
):

    bbox = [
        min_lon,
        min_lat,
        max_lon,
        max_lat
    ]

    items = search_sentinel2(
        bbox=bbox,
        start_date=start_date,
        end_date=end_date,
        cloud_cover=cloud_cover,
        limit=limit
    )

    results = []

    for item in items:

        results.append({
            "id": item.id,

            "datetime": (
                item.datetime.isoformat()
                if item.datetime
                else None
            ),

            "cloud_cover": item.properties.get(
                "eo:cloud_cover"
            ),

            "bbox": item.bbox,

            "assets": list(item.assets.keys())
        })

    return {
        "count": len(results),
        "results": results
    }