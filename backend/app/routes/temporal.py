from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.temporal_services import analyze_timeline


router = APIRouter(
    prefix="/api/temporal",
    tags=["Multi-Temporal Analysis"]
)


class Observation(BaseModel):
    image_id: str
    scene_id: str
    date: str
    image_path: str


class TemporalRequest(BaseModel):
    scene_id: str
    observations: list[Observation] = Field(min_length=2)


@router.post("/analyze")
def temporal_analysis(request: TemporalRequest):

    observations: list[dict[str, Any]] = [
        observation.model_dump()
        for observation in request.observations
    ]

    try:
        result = analyze_timeline(observations)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

    return {
        "success": True,
        "is_demo": True,
        **result
    }