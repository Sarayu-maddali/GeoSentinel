from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.review_service import (
    create_review,
    get_reviews,
    update_review
)


router = APIRouter(
    prefix="/api/reviews",
    tags=["Analyst Review"]
)


class CreateReviewRequest(BaseModel):
    candidate_id: str
    analyst: str = "Analyst 01"
    model_confidence: float | None = None


class UpdateReviewRequest(BaseModel):
    decision: str
    comment: str = ""
    analyst: str = "Analyst 01"


@router.get("")
def reviews():

    return {
        "success": True,
        "reviews": get_reviews(),
        "is_demo": True
    }


@router.post("")
def add_review(request: CreateReviewRequest):

    review = create_review(
        candidate_id=request.candidate_id,
        analyst=request.analyst,
        model_confidence=request.model_confidence
    )

    return {
        "success": True,
        "review": review,
        "is_demo": True
    }


@router.patch("/{review_id}")
def edit_review(
    review_id: str,
    request: UpdateReviewRequest
):

    try:
        review = update_review(
            review_id=review_id,
            decision=request.decision,
            comment=request.comment,
            analyst=request.analyst
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return {
        "success": True,
        "review": review,
        "is_demo": True
    }