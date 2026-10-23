import os
import ee
import geemap

# --- GEOSPATIAL & PROJECT CONSTANTS ---
# Project CRS matching QGIS visual reference
DEFAULT_CRS = "EPSG:3857"

# CEMS Wildfire EMSR253 Data / AOI Defaults
DEFAULT_AOI_NAME = "EMSR253"
# Coordinates centered around your wildfire event region (Longitude, Latitude)
DEFAULT_CENTER = [38.2, 23.8]
DEFAULT_ZOOM = 10


def initialize_earth_engine(project_id: str = 'ee-zamarimaryam') -> bool:
    """
    Authenticates and initializes the Google Earth Engine API.

    Args:
        project_id (str, optional): Google Cloud Project ID required for GEE API v1+.
                                    Defaults to EE_PROJECT_ID environment variable if set.
    Returns:
        bool: True if initialization succeeded, False otherwise.
    """
    ee_project = project_id or os.getenv("ee-zamarimaryam")

    try:
        if ee_project:
            ee.Initialize(project=ee_project)
        else:
            ee.Initialize()
        print("[INFO] Google Earth Engine initialized successfully.")
        return True

    except Exception:
        print("[WARNING] Earth Engine initialization failed. Attempting interactive authentication...")
        try:
            ee.Authenticate()
            if ee_project:
                ee.Initialize(project=ee_project)
            else:
                ee.Initialize()
            print("[INFO] Google Earth Engine authenticated and initialized successfully.")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to initialize Google Earth Engine: {e}")
            return False


if __name__ == "__main__":
    # Test execution when running config.py directly
    initialize_earth_engine()

