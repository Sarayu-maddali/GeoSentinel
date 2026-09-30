from fastapi import APIRouter, HTTPException

from app.services.provenance_service import (
    get_provenance
)


router = APIRouter(
    prefix="/api/provenance",
    tags=["Provenance"]
)


@router.get("/{scene_id}")
def provenance(scene_id: str):

    result = get_provenance(scene_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Provenance not found"
        )

    return {
        "success": True,
        "provenance": result,
        "is_demo": True
    }