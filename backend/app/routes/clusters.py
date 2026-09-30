from fastapi import APIRouter, HTTPException

from app.services.cluster_service import (
    get_cluster,
    get_clusters
)


router = APIRouter(
    prefix="/api/clusters",
    tags=["Clustering"]
)


@router.get("")
def clusters():
    return {
        "success": True,
        "count": len(get_clusters()),
        "clusters": get_clusters(),
        "is_demo": True
    }


@router.get("/{cluster_id}")
def cluster(cluster_id: int):

    result = get_cluster(cluster_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Cluster not found"
        )

    return {
        "success": True,
        "cluster": result,
        "is_demo": True
    }