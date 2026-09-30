from datetime import date

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.services.unified_search import unified_search


router = APIRouter(
    prefix="/api/search",
    tags=["Unified Search"]
)


class UnifiedSearchRequest(BaseModel):

    query: str = Field(min_length=1)

    bbox: list[float] | None = Field(default=None, min_length=4, max_length=4)

    start_date: str | None = None

    end_date: str | None = None

    satellites: list[str] | None = None

    cloud_cover: float | None = Field(default=None, ge=0, le=100)

    top_k: int = Field(default=20, ge=1, le=100)

    @field_validator("bbox")
    @classmethod
    def validate_bbox(cls, value):
        if value is not None and value[0] >= value[2]:
            raise ValueError("bbox must be [min_lon, min_lat, max_lon, max_lat]")
        if value is not None and value[1] >= value[3]:
            raise ValueError("bbox must be [min_lon, min_lat, max_lon, max_lat]")
        return value

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date(cls, value):
        if value is not None:
            try:
                date.fromisoformat(value)
            except ValueError as error:
                raise ValueError("dates must use YYYY-MM-DD format") from error
        return value


@router.post("/unified")
def search(request: UnifiedSearchRequest):

    try:
        result = unified_search(
            query=request.query,
            bbox=request.bbox,
            satellites=request.satellites,
            cloud_cover=request.cloud_cover,
            start_date=request.start_date,
            end_date=request.end_date
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    result["results"] = result["results"][
        :request.top_k
    ]

    return result