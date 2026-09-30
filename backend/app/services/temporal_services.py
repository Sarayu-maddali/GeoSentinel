from datetime import datetime
from typing import Any, Callable


def _parse_date(value: str) -> datetime:
    return datetime.fromisoformat(value)


def analyze_timeline(
    observations: list[dict[str, Any]],
    change_detector: Callable | None = None,
    confidence_threshold: float = 0.50,
) -> dict[str, Any]:
    """
    Compare chronological satellite observations pair-by-pair.

    Person 2 can later provide a real change_detector function.

    Expected detector result:
    {
        "change_detected": True,
        "confidence": 0.86,
        "change_type": "construction"
    }
    """

    if len(observations) < 2:
        raise ValueError("At least two observations are required.")

    observations = sorted(
        observations,
        key=lambda item: _parse_date(item["date"])
    )

    comparisons = []

    for index in range(len(observations) - 1):

        before = observations[index]
        after = observations[index + 1]

        if change_detector:
            result = change_detector(
                before["image_path"],
                after["image_path"]
            )
        else:
            # DEMONSTRATION ONLY.
            result = {
                "change_detected": False,
                "confidence": 0.0,
                "change_type": None,
                "is_demo": True
            }

        confidence = float(result.get("confidence", 0.0))
        detected = bool(
            result.get("change_detected", False)
            and confidence >= confidence_threshold
        )

        comparisons.append({
            "before_date": before["date"],
            "after_date": after["date"],
            "before_image_id": before.get("image_id"),
            "after_image_id": after.get("image_id"),
            "change_detected": detected,
            "confidence": confidence,
            "change_type": result.get("change_type"),
            "mask_url": result.get("mask_url"),
            "is_demo": result.get("is_demo", False)
        })

    first_change = next(
        (
            comparison
            for comparison in comparisons
            if comparison["change_detected"]
        ),
        None
    )

    return {
        "scene_id": observations[0].get("scene_id"),
        "observation_count": len(observations),
        "comparison_count": len(comparisons),
        "first_change_date": (
            first_change["after_date"]
            if first_change
            else None
        ),
        "first_change_type": (
            first_change["change_type"]
            if first_change
            else None
        ),
        "timeline": comparisons
    }