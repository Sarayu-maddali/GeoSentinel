import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

REVIEWS_FILE = DATA_DIR / "reviews.json"


def _load() -> list:
    if not REVIEWS_FILE.exists():
        return []

    with open(REVIEWS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def _save(reviews: list):
    with open(
        REVIEWS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            reviews,
            file,
            indent=2
        )


def get_reviews():
    return _load()


def create_review(
    candidate_id: str,
    analyst: str,
    model_confidence: float | None = None
):

    reviews = _load()

    review = {
        "id": str(uuid4()),
        "candidate_id": candidate_id,
        "status": "PENDING",
        "analyst": analyst,
        "comment": "",
        "model_confidence": model_confidence,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "updated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "audit": []
    }

    reviews.append(review)
    _save(reviews)

    return review


def update_review(
    review_id: str,
    decision: str,
    comment: str,
    analyst: str
):

    allowed = {
        "PENDING",
        "CONFIRMED",
        "REJECTED",
        "NEEDS_REVIEW"
    }

    if decision not in allowed:
        raise ValueError(
            f"Decision must be one of {sorted(allowed)}"
        )

    reviews = _load()

    for review in reviews:

        if review["id"] == review_id:

            timestamp = datetime.now(
                timezone.utc
            ).isoformat()

            review["status"] = decision
            review["comment"] = comment
            review["analyst"] = analyst
            review["updated_at"] = timestamp

            review["audit"].append({
                "analyst": analyst,
                "decision": decision,
                "comment": comment,
                "timestamp": timestamp
            })

            _save(reviews)

            return review

    return None