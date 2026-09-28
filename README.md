# SIH 2026 — Intelligent Hazard-Based Red Zone Identification & Relocation Decision Support System

> **Smart India Hackathon 2026**
> **Problem Statement:** SIH26191
> **Domain:** Disaster Management / GIS / Artificial Intelligence & Machine Learning

An AI- and GIS-powered decision-support platform for identifying **hazard-based red zones**, assessing the **exposure and vulnerability of habitations**, evaluating **carrying capacity of safer locations**, and supporting **pre-disaster relocation planning**.

The system is designed to assist **State and District Disaster Management Authorities** in making data-driven decisions before disasters occur.

---

## 📌 Problem Statement

Disaster-prone regions contain habitations that may be exposed to multiple hazards such as:

* Landslides
* Floods
* Coastal hazards
* Extreme rainfall
* Terrain-related risks

Existing disaster-management workflows often require authorities to analyze multiple datasets independently, making it difficult to identify vulnerable settlements and determine suitable relocation options efficiently.

This project proposes an integrated **GIS + Machine Learning decision-support platform** that combines hazard analysis, population screening, exposure, vulnerability, risk assessment, and relocation-site evaluation into a single system.

---

## 🎯 Objectives

The primary objectives of the system are to:

* Identify habitations located in potential hazard-prone areas.
* Analyze landslide, flood, rainfall, terrain, and coastal risk factors.
* Generate hazard and risk scores for settlements.
* Identify settlements requiring red-zone classification.
* Assess population exposure and vulnerability.
* Identify existing settlements with available carrying capacity.
* Identify potential new relocation sites.
* Perform site-safety and capacity analysis.
* Match vulnerable habitations with suitable relocation sites.
* Provide an interactive GIS-based dashboard for decision-makers.

---

## 🔄 System Workflow

```text
DATA COLLECTION
       ↓
DATA PREPROCESSING
       ↓
HABITATION MAPPING
       ↓
POPULATION SCREENING
       ↓
 ┌───────────────┬───────────────┬────────────────┐
 │               │               │                │
 ▼               ▼               ▼                ▼
LANDSLIDE ML   FLOOD ML     COASTAL ANALYSIS   TERRAIN
 │               │               │                │
 └───────────────┴───────────────┴────────────────┘
                       ↓
                 HAZARD SCORE
                       ↓
          EXPOSURE + VULNERABILITY
                       ↓
                  RISK SCORE
                       ↓
               RED ZONE DECISION
                       ↓
        ┌──────────────┴──────────────┐
        ↓                             ↓
EXISTING SETTLEMENTS             NEW SITES
WITH SPARE CAPACITY              / GREENFIELD
        │                             │
        └──────────────┬──────────────┘
                       ↓
                SITE SAFETY CHECK
                       ↓
                CAPACITY ANALYSIS
                       ↓
                  SITE MATCHING
                       ↓
                   RELOCATION
```

---

## 🧠 Core Components

### 1. GIS-Based Data Processing

The platform processes geospatial datasets and converts them into usable spatial features for analysis.

Key technologies include:

* GeoPandas
* Rasterio
* QGIS
* GeoJSON
* GeoPackage
* GeoTIFF
* Digital Elevation Models (DEM)

---

### 2. Terrain & Slope Analysis

Digital Elevation Model data is processed to derive terrain characteristics such as elevation and slope.

Slope information is used as one of the important factors in landslide susceptibility analysis.

---

### 3. Landslide Risk Analysis

Historical landslide data is processed and combined with terrain and environmental features.

The system includes a machine-learning pipeline for:

* Preparing training data
* Feature extraction
* Positive and negative sample generation
* Model training
* Landslide susceptibility prediction
* Susceptibility-map generation
* Red-zone identification

---

### 4. Flood Analysis

The system includes a flood-analysis module designed to incorporate environmental and spatial factors for identifying areas potentially exposed to flood hazards.

---

### 5. Coastal Hazard Analysis

A separate coastal-analysis component is included to support hazard assessment in coastal regions.

This allows the overall architecture to be extended beyond a single hazard type.

---

### 6. Population Screening

Population and habitation data are processed to identify settlements potentially exposed to hazardous regions.

The screening process helps connect:

```text
Hazard → Habitation → Population → Exposure → Risk
```

---

### 7. Hazard & Risk Scoring

Multiple hazard indicators can be combined to generate an overall hazard assessment.

The broader risk assessment considers:

```text
Risk = Hazard × Exposure × Vulnerability
```

The resulting assessment supports the identification of habitations that may require further investigation or relocation planning.

---

### 8. Red Zone Identification

The platform identifies settlements that satisfy defined hazard and risk conditions and classifies them as potential **red-zone habitations**.

The classification is intended as a decision-support output for disaster-management authorities rather than an autonomous replacement for official government decisions.

---

### 9. Carrying Capacity Assessment

For safer areas, the system evaluates whether existing settlements or potential sites have sufficient capacity to accommodate relocated populations.

Factors can include:

* Available area
* Existing population
* Settlement capacity
* Site safety
* Hazard exposure
* Accessibility
* Suitability

---

### 10. Relocation Site Matching

The final stage connects vulnerable habitations with potential safer locations.

```text
Vulnerable Habitation
        ↓
Risk Assessment
        ↓
Red Zone Identification
        ↓
Candidate Safe Sites
        ↓
Safety + Capacity Analysis
        ↓
Site Matching
        ↓
Relocation Recommendation
```

---

# 🖥️ Application

The project includes a web-based dashboard for interacting with the processed geospatial and machine-learning outputs.

The dashboard is intended to provide:

* District selection
* Interactive maps
* Hazard visualization
* Landslide susceptibility information
* Habitation information
* Population screening
* Red-zone visualization
* Relocation-site analysis

The system is primarily designed for **government and disaster-management decision-support use**.

---

# 🛠️ Technology Stack

## Programming

* Python
* HTML
* CSS
* JavaScript

## Artificial Intelligence / Machine Learning

* Scikit-learn
* Python-based ML pipelines
* Feature engineering
* Classification / susceptibility modelling

## GIS & Spatial Processing

* GeoPandas
* Rasterio
* QGIS
* Leaflet
* GeoJSON
* GeoPackage
* GeoTIFF
* DEM

## Database

* MySQL

## Web Application

* Flask
* HTML
* CSS
* JavaScript
* Leaflet

---

# 📁 Project Structure

```text
SIH-2026/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── database.py
│
├── ml/
│   ├── coastal_analysis.py
│   ├── flood_model.py
│   ├── landslide_model.py
│   ├── train_landslide_model.py
│   ├── create_red_zone.py
│   ├── create_susceptibility_map.py
│   └── find_red_zone_habitations.py
│
├── data/
│   ├── boundaries/
│   └── landslide/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
│
├── templates/
│   ├── dashboard.html
│   └── login.html
│
├── calculate_slope.py
├── extract_landslide_slope.py
├── create_negative_samples.py
├── prepare_habitations.py
├── prepare_landslides.py
├── prepare_ml_dataset.py
├── population_screening.py
├── map_habitations.py
│
└── inspect_*.py
```

> Large raster and geospatial processing outputs may be maintained separately from the source-code repository because of their file sizes.

---

# 📊 Data Pipeline

The project follows a multi-stage geospatial data pipeline.

### Step 1 — Data Collection

Sources can include:

* Digital Elevation Models
* Historical landslide inventories
* Rainfall datasets
* Administrative boundaries
* Habitation data
* Population data
* Spatial infrastructure data

### Step 2 — Preprocessing

Raw datasets are:

* Cleaned
* Reprojected where necessary
* Converted into compatible spatial formats
* Checked for missing values
* Prepared for feature extraction

### Step 3 — Feature Engineering

Relevant spatial and environmental features are extracted, including terrain-related characteristics and hazard indicators.

### Step 4 — Machine Learning

Prepared features are supplied to the relevant ML models for hazard/susceptibility prediction.

### Step 5 — Risk Assessment

Model outputs are combined with exposure and vulnerability information.

### Step 6 — Decision Support

The resulting information is visualized through the GIS dashboard to support red-zone and relocation planning.

---

# 🤖 Machine Learning Pipeline

The landslide analysis pipeline broadly follows:

```text
Historical Landslide Data
          ↓
Data Cleaning
          ↓
Spatial Feature Extraction
          ↓
Terrain / Environmental Features
          ↓
Training Dataset
          ↓
Positive + Negative Samples
          ↓
Model Training
          ↓
Susceptibility Prediction
          ↓
Susceptibility Map
          ↓
Red Zone Identification
```

---

# 🌍 Example Study Area

The current implementation includes spatial processing and analysis focused on **Pune district**, with the architecture designed to support additional districts.

The system can be extended by providing corresponding:

* Administrative boundaries
* DEM data
* Hazard datasets
* Rainfall/environmental data
* Habitation data
* Population data

---

# 🔐 Intended Users

The proposed system is intended primarily for:

* State Disaster Management Authorities
* District Disaster Management Authorities
* Disaster-management officers
* Government planning authorities
* GIS analysts
* Emergency planning teams

The platform is designed as a **decision-support system**, with final administrative and relocation decisions remaining with the responsible authorities.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Prithviraj3131/SIH-2026.git
cd SIH-2026
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the Database

Update the database configuration in:

```text
database/database.py
```

with your MySQL credentials and database details.

## 5. Run the Application

```bash
python app.py
```

The application will then be available through the local Flask server.

---

# 🗺️ GIS Processing

Processing scripts can be executed independently depending on the required workflow.

For example:

```bash
python calculate_slope.py
```

```bash
python prepare_landslides.py
```

```bash
python prepare_habitations.py
```

```bash
python prepare_ml_dataset.py
```

```bash
python ml/train_landslide_model.py
```

The exact execution order may depend on the available datasets and processing stage.

---

# 🔮 Future Scope

The platform can be further enhanced with:

* Real-time rainfall and weather feeds
* Satellite imagery integration
* Near-real-time disaster monitoring
* Advanced deep-learning models
* Multi-hazard risk fusion
* Road-network accessibility analysis
* Infrastructure vulnerability analysis
* Automated safe-site discovery
* Optimization-based relocation planning
* Multi-district and state-level deployment
* Role-based government access
* Audit logs and decision history
* Explainable AI for hazard predictions

---

# ⚠️ Data & Model Disclaimer

The outputs generated by this project are intended for **research, demonstration, and decision-support purposes**.

Machine-learning predictions and GIS-derived risk classifications should not be treated as definitive declarations of safety, danger, or mandatory relocation without appropriate validation, field assessment, and authorization by competent authorities.

---

# 👥 Project

**Smart India Hackathon 2026**

**Problem Statement:** SIH26191

**Project:** Intelligent Identification of Hazard-Based Red Zones, Carrying Capacity Assessment, and Immediate Relocation Needs for Vulnerable Habitations

**Repository:**
https://github.com/Prithviraj3131/SIH-2026

---

## ⭐ Project Vision

> **From hazard detection to informed relocation planning — using GIS, AI, machine learning, and spatial intelligence to support safer communities.**
