from typing import Any


# DEMONSTRATION DATA.
# Replace this with Person 2's actual embedding/clustering output.

DEMO_CLUSTERS = [
    {
        "cluster_id": 1,
        "label": "Dense Urban Expansion",
        "locations": [
            {
                "scene_id": "DEMO_SCENE_001",
                "latitude": 12.9716,
                "longitude": 77.5946,
                "similarity": 0.91
            },
            {
                "scene_id": "DEMO_SCENE_002",
                "latitude": 12.9352,
                "longitude": 77.6245,
                "similarity": 0.88
            }
        ]
    },
    {
        "cluster_id": 2,
        "label": "Agricultural",
        "locations": [
            {
                "scene_id": "DEMO_SCENE_003",
                "latitude": 13.0827,
                "longitude": 77.5877,
                "similarity": 0.84
            }
        ]
    },
    {
        "cluster_id": 3,
        "label": "Water-Adjacent Development",
        "locations": [
            {
                "scene_id": "DEMO_SCENE_004",
                "latitude": 12.9158,
                "longitude": 77.6101,
                "similarity": 0.82
            }
        ]
    }
]


def get_clusters() -> list[dict[str, Any]]:
    return DEMO_CLUSTERS


def get_cluster(cluster_id: int):
    for cluster in DEMO_CLUSTERS:
        if cluster["cluster_id"] == cluster_id:
            return cluster

    return None