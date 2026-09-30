import axios from "axios";

const API = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000",
    timeout: 12000,
});

const unwrap = (response) => response.data;

export async function searchUnified(filters) { return unwrap(await API.post("/api/search/unified", filters)); }
export async function analyzeTemporal(payload) { return unwrap(await API.post("/api/temporal/analyze", payload)); }
export async function getClusters() { return unwrap(await API.get("/api/clusters")); }
export async function getCluster(clusterId) { return unwrap(await API.get(`/api/clusters/${clusterId}`)); }
export async function getReviews() { return unwrap(await API.get("/api/reviews")); }
export async function createReview(payload) { return unwrap(await API.post("/api/reviews", payload)); }
export async function updateReview(reviewId, payload) { return unwrap(await API.patch(`/api/reviews/${reviewId}`, payload)); }
export async function getProvenance(sceneId) { return unwrap(await API.get(`/api/provenance/${encodeURIComponent(sceneId)}`)); }
export async function checkHealth() { return unwrap(await API.get("/health")); }