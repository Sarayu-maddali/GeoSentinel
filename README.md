#  GeoSentinel – Satellite Imagery Search System

GeoSentinel is a web-based satellite imagery search and discovery platform designed to make Earth observation data easier to search, explore, and retrieve.

The system provides a modern React-based frontend and a FastAPI backend that supports satellite imagery ingestion, STAC-based search, spatial and temporal filtering, provenance tracking, review workflows, and unified search.

GeoSentinel is designed to work with publicly accessible Earth observation datasets and STAC-compatible satellite imagery catalogs.

---

##  Problem Statement

Satellite imagery is available from multiple Earth observation missions and data providers. However, discovering the appropriate imagery for a particular location, time period, or requirement can be difficult because the data is distributed across different platforms and catalogs.

Users may need to manually search multiple sources, understand different metadata formats, and compare large numbers of satellite scenes.

GeoSentinel addresses this problem by providing a unified interface for discovering and searching satellite imagery using relevant search parameters.

---

##  Objectives

The main objectives of GeoSentinel are:

- Provide a unified interface for satellite imagery discovery.
- Simplify the process of searching Earth observation data.
- Support spatial and temporal satellite imagery search.
- Integrate STAC-based satellite data catalogs.
- Provide structured satellite imagery metadata.
- Support satellite imagery ingestion and processing.
- Provide provenance information for discovered datasets.
- Enable efficient search across available imagery.
- Provide a user-friendly web interface for interacting with satellite data.
- Create a foundation for scalable satellite imagery discovery and analysis.

---

##  Key Features

###  Satellite Imagery Search

Users can search for relevant satellite imagery using search parameters such as:

- Geographic location
- Spatial region
- Date and time
- Satellite/data source
- Available metadata
- Other supported search parameters

---

###  Spatial Search

The system supports searching satellite imagery based on geographic information.

This allows users to identify imagery associated with a particular:

- Location
- Area of interest
- Geographic region
- Spatial extent

---

###  Temporal Search

Users can search satellite imagery within a specified time period.

For example:

```text
Start Date → 2025-01-01
End Date   → 2025-01-31
```

## System Architecture

```text
                        ┌──────────────────────┐
                        │        USER          │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │   React + Vite UI    │
                        │      Frontend        │
                        └──────────┬───────────┘
                                   │
                              REST API
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │    FastAPI Backend   │
                        └──────────┬───────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
              ▼                    ▼                    ▼
       ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
       │   Search    │      │  Ingestion  │      │ Provenance  │
       │  Services   │      │  Services   │      │  Services   │
       └─────────────┘      └─────────────┘      └─────────────┘
              │                    │                    │
              └────────────────────┼────────────────────┘
                                   ▼
                        ┌──────────────────────┐
                        │ STAC / Earth         │
                        │ Observation Sources  │
                        └──────────────────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │ Processed Satellite  │
                        │ Imagery Metadata     │
                        └──────────────────────┘
```

##  Technology Stack

### Frontend
- React
- Vite
- JavaScript
- HTML
- CSS
- ESLint

### Backend
- Python
- FastAPI
- Uvicorn

### Satellite Data & Processing
- STAC (SpatioTemporal Asset Catalog)
- Satellite imagery metadata
- Earth observation data
- Geospatial data processing

### Development Tools
- Visual Studio Code
- Git
- GitHub
- npm
- Python Virtual Environment


##  Key Features

###  Satellite Imagery Search
GeoSentinel allows users to search for satellite imagery using relevant search parameters such as geographical location, date, and satellite/data source.

###  Spatial Search
Users can search for satellite imagery based on a specific geographic region or area of interest.

###  Temporal Search
The system supports searching imagery based on a specified time period or acquisition date.

###  STAC-Based Search
GeoSentinel uses the STAC (SpatioTemporal Asset Catalog) standard to organize and search satellite imagery metadata.

###  Imagery Ingestion
The system includes an ingestion workflow for collecting and processing satellite imagery metadata from available data sources.

###  Unified Search
The backend provides a unified search mechanism that allows satellite imagery information to be accessed through a common interface.

###  Metadata and Provenance
The system maintains metadata and provenance information associated with satellite imagery, allowing users to understand the source and properties of the retrieved data.

###  Search and Review
The backend contains modular services for search, temporal filtering, provenance, reviews, and clustering.


##  Project Structure

```text
GeoSentinel/
│
└── satellite-search-system/
    │
    ├── backend/
    │   ├── app/
    │   │   ├── data/
    │   │   ├── routes/
    │   │   ├── services/
    │   │   └── main.py
    │   │
    │   ├── requirements.txt
    │   ├── test_ingestion.py
    │   └── test_stac.py
    │
    ├── data/
    │   ├── embeddings/
    │   ├── processed/
    │   ├── raw/
    │   ├── results/
    │   └── tiles/
    │
    ├── docs/
    │   └── PS227_AUDIT.md
    │
    ├── frontend/
    │   ├── public/
    │   ├── src/
    │   │   ├── App.jsx
    │   │   ├── App.css
    │   │   ├── api.js
    │   │   ├── index.css
    │   │   └── main.jsx
    │   ├── index.html
    │   ├── package.json
    │   ├── package-lock.json
    │   ├── vite.config.js
    │   └── eslint.config.js
    │
    ├── models/
    │
    ├── scripts/
    │   ├── ingest_imagery.py
    │   └── search_stac.py
    │
    ├── .gitignore
    └── README.md
```

##  Installation and Setup

### Prerequisites

Before running GeoSentinel, make sure the following are installed:

- Python 3.10 or higher
- Node.js
- npm
- Git
- Visual Studio Code

Check the installed versions:

```bash
python --version
node --version
npm --version
git --version
```
##  Running the Complete System

GeoSentinel consists of a React + Vite frontend and a FastAPI backend.

The overall workflow is:

```text
User
  │
  ▼
React + Vite Frontend
  │
  │ REST API Requests
  ▼
FastAPI Backend
  │
  ├── Search Services
  ├── Temporal Services
  ├── STAC Services
  ├── Ingestion Services
  ├── Provenance Services
  ├── Review Services
  └── Clustering Services
  │
  ▼
Satellite / STAC Data Sources
```

### Terminal 1 – Start the Backend

Navigate to the backend directory:

```bash
cd backend
```
Activate the Python virtual environment.

## Windows
venv\Scripts\activate

Start the FastAPI backend server:

python -m uvicorn app.main:app --reload

The backend will start at:

http://127.0.0.1:8000

### Terminal 2 – Start the Frontend

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

## Satellite Data Sources

GeoSentinel is designed to work with publicly available Earth observation and satellite imagery sources.

The project supports or is designed to integrate with sources such as:

Copernicus Sentinel-1 – Synthetic Aperture Radar (SAR) imagery
Copernicus Sentinel-2 – Multispectral optical imagery
USGS Landsat Collection – Earth observation imagery
NRSC/ISRO Bhuvan – Indian geospatial and Earth observation data
STAC-compatible Earth observation catalogs

The exact data sources available to the application depend on the configured APIs, STAC catalogs, and access policies.


### STAC-Based Search

GeoSentinel uses the SpatioTemporal Asset Catalog (STAC) approach for organizing and discovering satellite imagery.

STAC provides standardized metadata for describing geospatial assets and enables satellite scenes to be searched using parameters such as:

Geographic location
Date and time
Satellite or platform
Collection
Cloud cover
Spatial extent
Available assets

## STAC Search Workflow

User Search Request
        │
        ▼
React Frontend
        │
        ▼
FastAPI Search Endpoint
        │
        ▼
Search Service
        │
        ▼
STAC Catalog / API
        │
        ▼
Satellite Scene Metadata
        │
        ▼
Filtering and Processing
        │
        ▼
Search Results
        │
        ▼
React Frontend
