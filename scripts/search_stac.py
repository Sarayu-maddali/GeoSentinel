from backend.app.services.stac_service import search_sentinel2


# Bengaluru area
bbox = [
    77.55, 12.90,
    77.65, 13.00
]


# Search dates
start_date = "2025-01-01"
end_date = "2025-03-01"


# Search Sentinel-2 imagery
items = search_sentinel2(
    bbox=bbox,
    start_date=start_date,
    end_date=end_date,
    cloud_cover=20,
    limit=10
)


print("\nNumber of images found:", len(items))


for item in items:

    print("\n-----------------------------")

    print("ID:", item.id)

    print("Date:", item.datetime)

    print(
        "Cloud cover:",
        item.properties.get("eo:cloud_cover")
    )

    print("Assets:")

    for asset_key in item.assets:
        print("  -", asset_key)