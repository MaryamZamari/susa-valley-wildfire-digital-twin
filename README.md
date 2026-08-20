# Susa Valley Wildfire Analysis & Digital Twin

A geospatial analysis and remote sensing pipeline designed to assess wildfire severity, burn area extraction, and post-fire vegetation recovery in the Susa Valley using Google Earth Engine (GEE) and Python.

---

## 📌 Project Overview

This project integrates satellite remote sensing data with spatial analysis to quantify wildfire impacts. It leverages Earth Engine Code Editor scripts for GEE data processing and Python notebooks/scripts for downstream geospatial workflows and digital twin visualization.

### Key Analysis Components
* **Burnt Area Extraction:** Post-fire and pre-fire Normalized Burn Ratio (NBR) analysis and classification against CEMS boundaries.
* **NDVI & Vegetation Recovery:** Histogram timeseries analysis and pre/post-fire median composite generation.
* **Burn Severity Classification:** Normalized burn severity indexing, thresholding, and CEMS boundary comparisons.

---

## 📁 Repository Structure

this repository consists of three main sections: 
1-legacy ---> containing traces of legacy analysis on GEE , before aggregating the analysis and producing the final files. 
2-main containing the finalised files 
    ├── BurntAreaExtraction/    # NBR scripts & post-fire area classification
    ├── NDVI/                   # Timeseries, histograms, & vegetation composite scripts
    ├── burn-severity/          # Final burn severity indexing & reviewed script models
    ├── docs/                   # Thesis documentation & report figures (optional)
    └── README.md               # Project documentation

3-
.

🚀 Getting Started
Prerequisites
Google Earth Engine Account: Active access to the GEE Platform.

Python 3.9+

Git

Installation & Setup
1.Clone the Repository:

git clone [https://github.com/MaryamZamari/susa-valley-wildfire-digital-twin.git](https://github.com/MaryamZamari/susa-valley-wildfire-digital-twin.git)


2.Create a Virtual Environment:
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

3.Install Dependencies:
pip install earthengine-api geemap geopandas rasterio matplotlib folium

4.earthengine authenticate
earthengine authenticate

🔧 Workflow & Usage
Earth Engine Processing: Run the relevant JavaScript/python scripts in BurntAreaExtraction/ and burn-severity/ to extract satellite metrics.

Local Python Analysis: Use Python to ingest exported raster/vector outputs for custom histograms, geospatial plotting, and statistical reporting.
