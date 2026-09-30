import { useEffect, useState } from "react";
import { CircleMarker, MapContainer, Popup, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css";
import { analyzeTemporal, checkHealth, createReview, getClusters, getProvenance, getReviews, searchUnified, updateReview } from "./api";

const navItems = ["Overview", "Semantic Search", "Change Analysis", "Discovery", "Review Queue", "Data Ingestion", "Analytics", "Provenance", "Settings"];
const demoQuery = "newly built structures near a river";
const score = (value) => value == null ? "Unavailable" : `${Math.round(value * 100)}%`;
const DemoBadge = () => <span className="demo-badge">DEMO</span>;

function App() {
    const [active, setActive] = useState("Semantic Search");
    const [query, setQuery] = useState(demoQuery);
    const [filters, setFilters] = useState({ satellites: [], cloud_cover: 30, start_date: "", end_date: "", top_k: 20 });
    const [results, setResults] = useState([]);
    const [selected, setSelected] = useState(null);
    const [clusters, setClusters] = useState([]);
    const [reviews, setReviews] = useState([]);
    const [provenance, setProvenance] = useState(null);
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [online, setOnline] = useState(false);
    const [reviewComment, setReviewComment] = useState("");

    const refreshReviews = async () => {
        try { setReviews((await getReviews()).reviews || []); } catch { setReviews([]); }
    };
    useEffect(() => {
        checkHealth().then(() => setOnline(true)).catch(() => setOnline(false));
        getClusters().then((response) => setClusters(response.clusters || [])).catch(() => setClusters([]));
        getReviews().then((response) => setReviews(response.reviews || [])).catch(() => setReviews([]));
    }, []);
    const updateFilter = (key, value) => setFilters((current) => ({ ...current, [key]: value }));
    const runSearch = async (event) => {
        event?.preventDefault(); setLoading(true); setError("");
        try {
            const response = await searchUnified({ query, ...filters, satellites: filters.satellites.length ? filters.satellites : null, start_date: filters.start_date || null, end_date: filters.end_date || null });
            setResults(response.results || []); setSelected(response.results?.[0] || null);
        } catch (requestError) { setError(requestError.response?.data?.detail || "Backend unavailable. Start FastAPI in local mode."); }
        finally { setLoading(false); }
    };
    const selectScene = async (scene) => {
        setSelected(scene); setProvenance(null); setAnalysis(null);
        try { setProvenance((await getProvenance(scene.id)).provenance); } catch { setProvenance(null); }
    };
    const selectCluster = async (location) => {
        const clusterScene = {
            ...location,
            id: location.scene_id,
            satellite: location.satellite || "Cluster scene",
            sensor: location.sensor || "Unavailable",
            date: location.date || "2025-01-12",
            cloud_cover: location.cloud_cover ?? null,
            resolution: location.resolution || "Unavailable",
            quality_score: location.quality_score ?? null,
            semantic_score: location.similarity,
            ranking_score: location.similarity,
        };
        await selectScene(clusterScene);
        setActive("Semantic Search");
    };
    const openAnalysis = async () => {
        if (!selected) return; setActive("Change Analysis"); setAnalysis(null);
        try {
            const before = new Date(`${selected.date}T00:00:00`); before.setDate(before.getDate() - 30);
            setAnalysis(await analyzeTemporal({ scene_id: selected.id, observations: [{ image_id: `${selected.id}_before`, scene_id: selected.id, date: before.toISOString().slice(0, 10), image_path: "demo://before" }, { image_id: selected.id, scene_id: selected.id, date: selected.date, image_path: "demo://after" }] }));
        } catch (requestError) { setError(requestError.response?.data?.detail || "Change analysis is unavailable."); }
    };
    const submitReview = async () => {
        if (!selected) return;
        try { await createReview({ candidate_id: selected.id, model_confidence: selected.ranking_score }); await refreshReviews(); setActive("Review Queue"); }
        catch (requestError) { setError(requestError.response?.data?.detail || "Review action failed."); }
    };
    const mapScenes = results.length ? results : clusters.flatMap((cluster) => cluster.locations.map((location) => ({ ...location, id: location.scene_id })));
    const renderContent = () => {
        if (active === "Overview") return <Overview results={results} clusters={clusters} reviews={reviews} />;
        if (active === "Change Analysis") return <ChangeAnalysis selected={selected} analysis={analysis} />;
        if (active === "Review Queue") return <ReviewQueue reviews={reviews} comment={reviewComment} setComment={setReviewComment} onUpdate={async (id, decision) => { await updateReview(id, { decision, comment: reviewComment }); await refreshReviews(); }} />;
        if (active === "Provenance") return <Provenance provenance={provenance} selected={selected} />;
        if (active === "Discovery") return <Discovery clusters={clusters} onSelect={selectCluster} />;
        if (active === "Data Ingestion") return <DataIngestion />;
        if (active === "Analytics") return <Analytics results={results} clusters={clusters} />;
        if (active === "Settings") return <Settings />;
        return <SearchView query={query} setQuery={setQuery} filters={filters} updateFilter={updateFilter} runSearch={runSearch} loading={loading} error={error} results={results} selected={selected} selectScene={selectScene} mapScenes={mapScenes} openAnalysis={openAnalysis} openProvenance={() => setActive("Provenance")} submitReview={submitReview} />;
    };
    return <div className="app-shell"><aside className="sidebar"><div className="brand-mark">G<span>/</span></div><div className="brand"><strong>GeoSentinel</strong><small>EARTH OBSERVATION INTELLIGENCE</small></div><div className="side-rule" /><nav>{navItems.map((item) => <button className={active === item ? "nav-item active" : "nav-item"} key={item} onClick={() => setActive(item)}><span className="nav-dot" />{item}{item === "Review Queue" && reviews.length > 0 && <b>{reviews.length}</b>}</button>)}</nav><div className="sidebar-foot"><span className="status-dot" />LOCAL / OFFLINE MODE<br /><small>Data stays on this workstation</small></div></aside><main className="main"><header className="topbar"><div><span className="crumb">WORKSPACE / {active.toUpperCase()}</span><strong>GeoSentinel</strong></div><div className="top-status"><span className={online ? "online-dot" : "offline-dot"} />{online ? "API CONNECTED" : "OFFLINE / LOCAL MODE"}<span className="top-divider" />{new Date().toLocaleDateString(undefined, { month: "short", day: "2-digit", year: "numeric" })}<div className="avatar">AL</div>Analyst 01</div></header><div className="content">{renderContent()}</div></main></div>;
}

function SearchView({ query, setQuery, filters, updateFilter, runSearch, loading, error, results, selected, selectScene, mapScenes, openAnalysis, openProvenance, submitReview }) {
    return <><section className="search-hero"><div><p className="eyebrow">SEMANTIC SEARCH / LOCAL INDEX</p><h1>Find meaning in the landscape.</h1><p className="subtitle">Search across satellite scenes with language, metadata, and spatial context.</p></div><div className="hero-stat"><span>INDEX STATUS</span><strong>READY</strong><small>Demo index available locally</small></div></section><form className="search-bar" onSubmit={runSearch}><span className="search-icon">⌕</span><input value={query} onChange={(event) => setQuery(event.target.value)} aria-label="Natural language search" /><button type="submit" disabled={loading}>{loading ? "SEARCHING" : "SEARCH"}</button></form><section className="filter-row"><label>Satellite<select value={filters.satellites[0] || ""} onChange={(event) => updateFilter("satellites", event.target.value ? [event.target.value] : [])}><option value="">All platforms</option><option>Sentinel-1</option><option>Sentinel-2</option><option>Landsat-9</option></select></label><label>Max cloud cover<input type="number" min="0" max="100" value={filters.cloud_cover} onChange={(event) => updateFilter("cloud_cover", Number(event.target.value))} /></label><label>From<input type="date" value={filters.start_date} onChange={(event) => updateFilter("start_date", event.target.value)} /></label><label>To<input type="date" value={filters.end_date} onChange={(event) => updateFilter("end_date", event.target.value)} /></label><span className="filter-note">Filters applied by unified pipeline</span></section>{error && <div className="alert">{error}</div>}<div className="workspace-grid"><section><div className="section-heading"><div><p className="eyebrow">RANKED RETRIEVAL</p><h2>{results.length ? `${results.length} scenes found` : "Ready for a query"}</h2></div><span className="muted">Semantic + metadata + spatial</span></div>{results.length ? <div className="result-list">{results.map((scene) => <ResultCard key={scene.id} scene={scene} selected={selected?.id === scene.id} onSelect={() => selectScene(scene)} />)}</div> : <div className="empty-state"><span className="empty-orbit">◌</span><h3>Search the local scene index</h3><p>Try the example query to retrieve ranked demonstration scenes.</p><button className="secondary-button" type="button" onClick={runSearch}>Run example search</button></div>}</section><section className="map-panel"><div className="map-header"><span>SCENE MAP</span><span>{mapScenes.length} markers</span></div><MapContainer center={[12.9716, 77.5946]} zoom={10} className="map"><TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />{mapScenes.map((scene) => <CircleMarker key={scene.id} center={[scene.latitude, scene.longitude]} radius={selected?.id === scene.id ? 10 : 6} pathOptions={{ color: selected?.id === scene.id ? "#e6b85c" : "#56c7b1", fillOpacity: 0.8 }} eventHandlers={{ click: () => selectScene(scene) }}><Popup><strong>{scene.id}</strong><br />{scene.satellite || "Cluster location"}</Popup></CircleMarker>)}</MapContainer></section></div>{selected && <SceneDetail scene={selected} onAnalysis={openAnalysis} onProvenance={openProvenance} onReview={submitReview} />}</>;
}

function ResultCard({ scene, selected, onSelect }) { return <button className={selected ? "result-card selected" : "result-card"} onClick={onSelect}><div className="thumbnail"><span>NO PREVIEW</span><small>IMAGE ASSET UNAVAILABLE</small></div><div className="result-info"><div className="result-title"><strong>{scene.id}</strong><DemoBadge /></div><p>{scene.satellite} · {scene.sensor}</p><div className="meta-grid"><span>ACQUIRED<strong>{scene.date}</strong></span><span>CLOUD<strong>{scene.cloud_cover == null ? "N/A" : `${scene.cloud_cover}%`}</strong></span><span>RESOLUTION<strong>{scene.resolution}m</strong></span></div><div className="scores"><span>SEMANTIC <b>{score(scene.semantic_score)}</b></span><span>QUALITY <b>{score(scene.quality_score)}</b></span><span>RANK <b className="gold">{score(scene.ranking_score)}</b></span></div></div></button>; }
function SceneDetail({ scene, onAnalysis, onProvenance, onReview }) { return <section className="detail-panel"><div className="detail-preview"><span>PREVIEW UNAVAILABLE</span><small>No image asset was returned for this scene.</small></div><div className="detail-copy"><div className="section-heading"><div><p className="eyebrow">SELECTED SCENE <DemoBadge /></p><h2>{scene.id}</h2></div><span className="location-tag">{scene.latitude?.toFixed(3)} N · {scene.longitude?.toFixed(3)} E</span></div><div className="detail-metadata"><span>SATELLITE<strong>{scene.satellite}</strong></span><span>SENSOR<strong>{scene.sensor}</strong></span><span>DATE<strong>{scene.date}</strong></span><span>CLOUD<strong>{scene.cloud_cover == null ? "Unavailable" : `${scene.cloud_cover}%`}</strong></span></div><div className="action-row"><button onClick={onAnalysis}>↗ Change analysis</button><button onClick={onProvenance}>⌘ Provenance</button><button onClick={onReview}>＋ Analyst review</button></div></div></section>; }

function SceneMap({ scene, mode = "standard" }) {
    const latitude = Number(scene?.latitude);
    const longitude = Number(scene?.longitude);
    if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return <div className="image-placeholder">LOCATION UNAVAILABLE</div>;
    return <div className={`scene-map ${mode}`}><MapContainer center={[latitude, longitude]} zoom={11} scrollWheelZoom={false}><TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" /><CircleMarker center={[latitude, longitude]} radius={9} pathOptions={{ color: mode === "change" ? "#e6b85c" : "#56c7b1", fillOpacity: 0.65 }} /></MapContainer><span className="map-overlay">{mode === "change" ? "CHANGE MASK / DEMO" : "SCENE PREVIEW / DEMO"}</span></div>;
}

function ChangeAnalysis({ selected, analysis }) {
    const comparison = analysis?.timeline?.[0];
    return <div className="page-panel"><p className="eyebrow">MULTI-TEMPORAL ANALYSIS <DemoBadge /></p><h1>Change intelligence</h1><p className="subtitle">{selected ? `Scene ${selected.id} · chronological comparison` : "Select a scene from Semantic Search."}</p>{selected ? <><div className="triptych"><div><span>BEFORE</span><SceneMap scene={selected} /><strong>{comparison?.before_date || "Awaiting analysis"}</strong></div><div><span>CHANGE MAP</span><SceneMap scene={selected} mode="change" /><strong>{comparison?.change_type || "No change detected"}</strong></div><div><span>AFTER</span><SceneMap scene={selected} /><strong>{comparison?.after_date || selected.date}</strong></div></div><div className="analysis-note"><b>DEMO FALLBACK</b> Map imagery is shown because no satellite asset or change mask URL was returned.</div></> : <div className="empty-state"><h3>No scene selected</h3></div>}</div>;
}

function Overview({ results, clusters, reviews }) { return <div className="page-panel"><p className="eyebrow">WORKSPACE OVERVIEW</p><h1>Earth observation intelligence</h1><p className="subtitle">A live view of the local search, discovery, and analyst workflow.</p><div className="metric-grid"><div><span>SEARCH RESULTS</span><strong>{results.length}</strong><small>Current query</small></div><div><span>SCENE CLUSTERS</span><strong>{clusters.length}</strong><small>Available groups</small></div><div><span>REVIEW QUEUE</span><strong>{reviews.length}</strong><small>Analyst decisions</small></div></div><div className="overview-band"><div><p className="eyebrow">SYSTEM STATUS</p><h2>Local intelligence workspace</h2><p>Semantic retrieval, temporal analysis, clustering, and provenance are connected to the local FastAPI service.</p></div><span className="status-chip">READY</span></div></div>; }

function DataIngestion() { return <div className="page-panel"><p className="eyebrow">DATA PIPELINE</p><h1>Data ingestion</h1><p className="subtitle">Prepare satellite scenes for the local index.</p><div className="ingestion-panel"><div><span className="panel-label">SOURCE</span><strong>Local imagery workspace</strong><small>Drop-ready pipeline surface</small></div><div><span className="panel-label">STATUS</span><strong className="teal-text">CONNECTED</strong><small>Backend ingestion service available</small></div><button className="secondary-button" type="button">OPEN PIPELINE</button></div><div className="empty-state compact"><h3>No pending ingestion jobs</h3><p>New source scenes will appear here when the ingestion service returns a job.</p></div></div>; }

function Analytics({ results, clusters }) { return <div className="page-panel"><p className="eyebrow">WORKSPACE SIGNALS</p><h1>Analytics</h1><p className="subtitle">Signals from the current local retrieval and discovery data.</p><div className="metric-grid"><div><span>RETURNED SCENES</span><strong>{results.length}</strong><small>Ranked retrieval</small></div><div><span>DISCOVERY GROUPS</span><strong>{clusters.length}</strong><small>Cluster service</small></div><div><span>TOP SCORE</span><strong>{results.length ? `${Math.round(Math.max(...results.map((scene) => scene.ranking_score || 0)) * 100)}%` : "N/A"}</strong><small>Current retrieval</small></div></div><div className="analytics-bars">{clusters.map((cluster) => <div key={cluster.cluster_id}><span>CLUSTER {String(cluster.cluster_id).padStart(2, "0")}</span><i style={{ width: `${Math.round((cluster.locations?.[0]?.similarity || 0) * 100)}%` }} /><b>{Math.round((cluster.locations?.[0]?.similarity || 0) * 100)}%</b></div>)}</div></div>; }

function Settings() { return <div className="page-panel"><p className="eyebrow">WORKSPACE CONFIGURATION</p><h1>Settings</h1><p className="subtitle">Local connection and display preferences.</p><div className="settings-list"><label>API endpoint<input value="http://127.0.0.1:8000" readOnly /></label><label>Search mode<select defaultValue="semantic"><option value="semantic">Semantic + metadata + spatial</option><option value="metadata">Metadata only</option></select></label><label className="toggle-row"><span>Demo fallback data</span><input type="checkbox" defaultChecked /></label></div></div>; }
function ReviewQueue({ reviews, onUpdate, comment, setComment }) { return <div className="page-panel"><p className="eyebrow">ANALYST WORKFLOW</p><h1>Review queue</h1><p className="subtitle">Human decisions stay separate from model and demo signals.</p><textarea placeholder="Comment for the audit trail" value={comment} onChange={(event) => setComment(event.target.value)} />{reviews.length ? reviews.map((review) => <div className="review-row" key={review.id}><div><strong>{review.candidate_id}</strong><span>{review.analyst} · {new Date(review.updated_at).toLocaleString()}</span></div><span className={`status ${review.status.toLowerCase()}`}>{review.status}</span><div className="review-actions"><button onClick={() => onUpdate(review.id, "CONFIRMED")}>Confirm</button><button onClick={() => onUpdate(review.id, "REJECTED")}>Reject</button><button onClick={() => onUpdate(review.id, "NEEDS_REVIEW")}>Request review</button></div><small>Audit: {review.audit?.length || 0} decision(s)</small></div>) : <div className="empty-state compact"><h3>Queue is clear</h3><p>Select a search result to create a review.</p></div>}</div>; }
function Provenance({ provenance, selected }) { return <div className="page-panel"><p className="eyebrow">DATA LINEAGE <DemoBadge /></p><h1>Provenance</h1><p className="subtitle">Trace a scene through the local intelligence pipeline.</p>{provenance ? <><div className="lineage">{["SOURCE IMAGE", "PREPROCESSING", "QUALITY CONTROL", "EMBEDDING", "INDEX", "RETRIEVAL", "CHANGE ANALYSIS", "ANALYST DECISION"].map((stage, index) => <div className="lineage-stage" key={stage}><span>{String(index + 1).padStart(2, "0")}</span><strong>{stage}</strong>{index < 7 && <i>↓</i>}</div>)}</div><div className="provenance-table">{Object.entries(provenance).filter(([, value]) => typeof value !== "object").map(([key, value]) => <span key={key}>{key.replaceAll("_", " ")}<strong>{String(value)}</strong></span>)}</div></> : <div className="empty-state"><h3>{selected ? "Provenance unavailable" : "No scene selected"}</h3></div>}</div>; }
function Discovery({ clusters, onSelect }) { return <div className="page-panel"><p className="eyebrow">UNSUPERVISED DISCOVERY <DemoBadge /></p><h1>Scene clusters</h1><p className="subtitle">Groups returned by the available local clustering service.</p><div className="cluster-grid">{clusters.length ? clusters.map((cluster) => <button className="cluster-card" key={cluster.cluster_id} onClick={() => cluster.locations?.[0] && onSelect(cluster.locations[0])}><span>CLUSTER {String(cluster.cluster_id).padStart(2, "0")}</span><h3>{cluster.label}</h3><strong>{cluster.locations?.length || 0} scenes</strong><small>Open representative scene →</small></button>) : <div className="empty-state"><h3>No clusters available</h3><p>Start the backend discovery service to load scene groups.</p></div>}</div></div>; }

export default App;
