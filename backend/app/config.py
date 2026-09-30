import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:sarabhai1@localhost:5432/satellite_db"
)

STAC_URL = os.getenv(
    "STAC_URL",
    "https://stac.dataspace.copernicus.eu/v1"
)