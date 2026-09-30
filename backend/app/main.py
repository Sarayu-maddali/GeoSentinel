from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.search import router as search_router
from app.routes.temporal import router as temporal_router
from app.routes.clusters import router as clusters_router
from app.routes.reviews import router as reviews_router
from app.routes.provenance import router as provenance_router
from app.routes.unified_search import router as unified_search_router


app = FastAPI(
    title="Satellite Semantic Search System",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Existing semantic search routes
app.include_router(
    search_router,
    prefix="/api"
)


# Person 3 - Multi-temporal analysis
app.include_router(
    temporal_router
)


# Person 3 - Clustering
app.include_router(
    clusters_router
)


# Person 3 - Analyst review
app.include_router(
    reviews_router
)


# Person 3 - Provenance
app.include_router(
    provenance_router
)


# Person 3 - Unified search
app.include_router(
    unified_search_router
)


@app.get("/")
def root():

    return {
        "message": "Satellite Search API is running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }