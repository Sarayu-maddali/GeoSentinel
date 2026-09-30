from app.services.stac_service import search_sentinel2


# Bengaluru area
bbox = [
    77.55, 12.90,
    77.65, 13.00
]


# Date range
start_date = "2025-01-01"
end_date = "2025-03-01"


# Maximum cloud cover
cloud_cover = 20


# Maximum number of images
limit = 10


# Search Sentinel-2
items = search_sentinel2(
    bbox=bbox,
    start_date=start_date,
    end_date=end_date,
    cloud_cover=cloud_cover,
    limit=limit
)


print("\nNumber of images found:", len(items))


for item in items:

    print("\n-----------------------------")

    print("Image ID:", item.id)

    print("Date:", item.datetime)

    print(
        "Cloud cover:",
        item.properties.get("eo:cloud_cover")
    )

    print("Bounding box:", item.bbox)

    print("Assets:")

    for asset_key in item.assets:
        print("  -", asset_key)