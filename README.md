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

 

## Frontend Execution

After starting the backend, open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the required dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

Open this URL in your browser to access the GeoSentinel application.

---

## Core System Modules

GeoSentinel is organized into multiple modular components, each responsible for a specific part of the satellite imagery discovery process.

### 1. Search Service

The Search Service handles user search requests and retrieves relevant satellite imagery metadata.

Responsibilities:
- Accept search parameters from the frontend.
- Process geographic and temporal search criteria.
- Communicate with configured STAC catalogs.
- Retrieve matching satellite imagery records.
- Return structured search results.

### 2. Spatial Search Service

The Spatial Search Service enables users to discover satellite imagery associated with specific geographic regions.

It supports:
- Area of Interest (AOI) selection.
- Geographic coordinates.
- Bounding box-based search.
- Spatial extent filtering.

### 3. Temporal Search Service

The Temporal Search Service allows users to filter satellite imagery based on acquisition dates.

Responsibilities:
- Accept start and end dates.
- Identify imagery available within the selected period.
- Filter results based on acquisition timestamps.
- Support time-based imagery comparison.

### 4. STAC Integration Service

The STAC Integration Service connects GeoSentinel with external satellite imagery catalogs.

Responsibilities:
- Communicate with STAC APIs.
- Retrieve collection information.
- Search satellite imagery items.
- Extract metadata and asset information.
- Convert catalog responses into a unified format.

### 5. Imagery Ingestion Service

The Ingestion Service manages the collection and organization of satellite imagery information.

The workflow includes:

1. Connect to configured satellite data sources.
2. Retrieve available imagery metadata.
3. Extract relevant spatial and temporal information.
4. Organize the retrieved metadata.
5. Store processed information for further operations.

### 6. Provenance Service

The Provenance Service maintains information about the origin and characteristics of satellite imagery.

It helps users understand:
- Original data provider.
- Satellite mission and platform.
- Acquisition date.
- Collection information.
- Source catalog.
- Associated metadata and asset references.

### 7. Review Service

The Review Service provides a workflow for examining and validating retrieved satellite imagery records.

It can support:
- Reviewing discovered imagery.
- Inspecting metadata.
- Marking records for further verification.
- Maintaining review status.
- Supporting human-in-the-loop validation.

### 8. Clustering Service

The Clustering Service provides a foundation for grouping similar satellite imagery records.

Potential grouping criteria include:
- Geographic similarity.
- Acquisition time.
- Satellite mission.
- Collection type.
- Similarity between extracted image features.

---

## Data Processing Workflow

GeoSentinel follows a structured workflow to retrieve and organize satellite imagery information.

```text
User Search Input
       |
       v
Search Parameter Validation
       |
       v
Spatial and Temporal Filtering
       |
       v
STAC Catalog Communication
       |
       v
Satellite Metadata Retrieval
       |
       v
Metadata Extraction
       |
       v
Data Processing and Organization
       |
       v
Provenance Information
       |
       v
Search Results Generation
       |
       v
Display Results on Frontend
```

This workflow provides a common approach for discovering satellite imagery from multiple supported sources.

---

## Unified Search Mechanism

One of the main objectives of GeoSentinel is to simplify satellite imagery discovery through a unified search interface.

Instead of requiring users to manually explore multiple satellite data platforms, GeoSentinel provides a common interface for submitting search requests.

The unified search process involves:

1. Collecting user search parameters.
2. Identifying the relevant satellite data sources.
3. Sending requests to supported STAC catalogs.
4. Retrieving matching imagery records.
5. Applying spatial and temporal filters.
6. Organizing the retrieved metadata.
7. Presenting the results through the frontend.

This approach makes satellite imagery discovery more accessible and organized.

---

## API Communication

The React frontend communicates with the FastAPI backend through REST API endpoints.

The backend processes incoming requests and returns structured responses, generally in JSON format.

Example API structure:

| API Endpoint | Purpose |
|---|---|
| `/` | Backend status |
| `/docs` | Interactive API documentation |
| `/openapi.json` | API specification |
| `/search` | Satellite imagery search, if implemented |
| `/ingest` | Imagery metadata ingestion, if implemented |
| `/provenance` | Provenance information, if implemented |

**Note:** The actual endpoints depend on the routes implemented in the backend. FastAPI automatically generates interactive API documentation.

To access the API documentation, start the backend and open:

```text
http://127.0.0.1:8000/docs
```

---

## Data Storage and Organization

GeoSentinel uses a structured directory system to organize satellite imagery data and processing outputs.

The project separates raw data, processed information, embeddings, and search results.

| Directory | Description |
|---|---|
| `data/raw/` | Original or downloaded satellite data |
| `data/processed/` | Processed imagery and metadata |
| `data/embeddings/` | Feature embeddings for similarity-based search |
| `data/results/` | Search and processing outputs |
| `data/tiles/` | Generated geospatial tiles, when available |
| `models/` | Machine learning or feature extraction models |

This organization helps maintain a clear separation between input data, processing operations, and generated outputs.

---

## Error Handling and Validation

GeoSentinel incorporates backend validation and error handling to improve system reliability.

The system should handle situations such as:

- Invalid geographic coordinates.
- Incorrect date ranges.
- Missing search parameters.
- Unavailable STAC catalogs.
- Network connection failures.
- Empty search results.
- Invalid or incomplete metadata.

FastAPI provides request validation, while the frontend can display appropriate messages to help users understand search errors.

---

## Testing and Validation

Testing is important to verify that the individual components of GeoSentinel function correctly.

The project includes testing scripts for STAC integration and imagery ingestion.

### STAC Integration Testing

```bash
python test_stac.py
```

This test can be used to validate the STAC catalog communication and search functionality.

### Imagery Ingestion Testing

```bash
python test_ingestion.py
```

This test can be used to verify the imagery ingestion workflow.

### Frontend Testing

Run the frontend development server:

```bash
npm run dev
```

Verify that:
- The frontend loads successfully.
- Search inputs accept valid parameters.
- API requests reach the backend.
- Search results are displayed correctly.
- Error messages are handled appropriately.

---

## Expected Output

GeoSentinel aims to provide users with an organized view of satellite imagery discovered through configured data catalogs.

The expected search output includes:

- Satellite or platform name.
- Dataset or collection name.
- Acquisition date.
- Geographic location.
- Spatial extent.
- Cloud cover information, when available.
- Available imagery assets.
- Original data source.
- Provenance information.

The availability of individual metadata fields depends on the satellite mission and the source catalog.

---

## Applications of GeoSentinel

GeoSentinel can support several Earth observation and geospatial discovery applications.

1. **Agriculture:** Discovering satellite imagery for monitoring agricultural regions and crop conditions.

2. **Environmental Monitoring:** Exploring imagery for forests, water bodies, and environmental changes.

3. **Disaster Management:** Discovering satellite scenes associated with floods, wildfires, and other natural disasters.

4. **Urban Development:** Exploring changes in urban areas and infrastructure over time.

5. **Land Use Analysis:** Identifying satellite imagery for studying land cover and land-use patterns.

6. **Research and Education:** Helping students and researchers discover relevant Earth observation datasets.

---

## Advantages of GeoSentinel

- Provides a unified interface for satellite imagery discovery.
- Reduces the need to manually explore multiple data catalogs.
- Supports spatial and temporal filtering.
- Uses the standardized STAC metadata framework.
- Provides structured satellite imagery information.
- Supports modular backend architecture.
- Maintains imagery source and provenance information.
- Provides a foundation for integrating additional satellite data providers.
- Can be extended with machine learning and geospatial analysis capabilities.

---

## Current Limitations

The functionality of GeoSentinel depends on the availability and configuration of external satellite data catalogs.

Some limitations include:

- Different data providers may expose different metadata fields.
- Certain satellite datasets may require authentication.
- Large satellite imagery files may require significant storage and processing resources.
- Network connectivity may affect external catalog searches.
- Some advanced imagery analysis capabilities require additional processing modules.
- The availability of imagery depends on the selected geographic region and time period.

---

## Future Enhancements

GeoSentinel can be extended with additional capabilities to improve satellite imagery discovery and analysis.

Planned enhancements include:

1. **AI-Based Semantic Search:** Enable users to search satellite imagery using natural-language descriptions instead of relying only on traditional search parameters.

2. **Image Embedding Generation:** Generate feature embeddings from satellite imagery to support content-based similarity search.

3. **Change Detection:** Compare satellite images acquired at different times to identify changes in land cover, vegetation, infrastructure, and other geographic features.

4. **Interactive Geospatial Visualization:** Integrate interactive maps for visualizing satellite imagery footprints and areas of interest.

5. **Advanced Image Filtering:** Introduce filters based on cloud cover, resolution, satellite sensor, and other metadata.

6. **Multi-Source Integration:** Expand support for additional Earth observation datasets and STAC-compatible catalogs.

7. **Satellite Image Clustering:** Group similar satellite scenes based on geographic, temporal, or visual characteristics.

8. **Scalable Data Processing:** Improve ingestion and processing workflows to support larger satellite imagery collections.

9. **Human-in-the-Loop Review:** Improve the review workflow to support verification and feedback on discovered imagery.

10. **Advanced Change Analysis Dashboard:** Provide visual comparisons and analytical summaries of satellite imagery from different time periods.

---

## Project Goals

GeoSentinel aims to make satellite imagery discovery more accessible by bringing different Earth observation data sources into a unified search platform.

By combining React, FastAPI, STAC integration, geospatial filtering, metadata processing, and provenance tracking, the project provides a modular foundation for building a scalable satellite imagery discovery system.

The long-term goal is to extend GeoSentinel beyond traditional metadata-based searching by incorporating AI-powered semantic discovery, image similarity search, and satellite imagery change analysis.

---

## Conclusion

GeoSentinel addresses the challenge of discovering satellite imagery distributed across multiple Earth observation platforms and data providers.

The platform combines a modern web interface with a modular backend to simplify satellite imagery search, support spatial and temporal filtering, integrate STAC-based catalogs, and organize satellite imagery metadata.

With its extensible architecture, GeoSentinel provides a foundation for advanced Earth observation applications and future integration of artificial intelligence, machine learning, and geospatial analytics.

---

## Author

**Project Name:** GeoSentinel – Satellite Imagery Search System

**Technology Stack:** React, Vite, Python, FastAPI, STAC

**Development Tools:** Visual Studio Code, Git, GitHub

**Domain:** Satellite Imagery, Geospatial Technology, Earth Observation, Data Science

