import pystac_client

from app.config import STAC_URL


# Connect to the Copernicus STAC catalogue
catalog = pystac_client.Client.open(STAC_URL)


def search_sentinel2(
    bbox,
    start_date,
    end_date,
    cloud_cover=30,
    limit=50
):
    """
    Search Sentinel-2 satellite imagery.

    Parameters:
        bbox: [min_lon, min_lat, max_lon, max_lat]
        start_date: starting date YYYY-MM-DD
        end_date: ending date YYYY-MM-DD
        cloud_cover: maximum allowed cloud percentage
        limit: maximum number of results

    Returns:
        List of Sentinel-2 STAC items
    """

    search = catalog.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime=f"{start_date}/{end_date}",
        query={
            "eo:cloud_cover": {
                "lte": cloud_cover
            }
        },
        max_items=limit
    )

    return list(search.items())