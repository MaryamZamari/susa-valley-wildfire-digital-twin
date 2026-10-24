import os
import ee

# --- GEOSPATIAL & PROJECT CONSTANTS ---
DEFAULT_CRS = "EPSG:3857"
DEFAULT_AOI_NAME = "EMSR253"

# Map display center [lat, lon] for geemap
DEFAULT_CENTER = [45.167, 7.119]
DEFAULT_ZOOM = 11

# Susa Valley EMSR253 study area coordinates [lon, lat]
EMSR253_COORDS_BB = [
    [
        [7.029021402162807, 45.21972611576043],
        [7.029021402162807, 45.1146736921262],
        [7.2092658479635885, 45.1146736921262],
        [7.2092658479635885, 45.21972611576043]
    ]
]

# EMSR253 Event Timeline (October 2017 Wildfire)
PRE_FIRE_START = "2017-09-15"
PRE_FIRE_END = "2017-10-15"
POST_FIRE_START = "2017-10-25"
POST_FIRE_END = "2017-11-20"



def initialize_earth_engine(project_id: str = 'ee-zamarimaryam') -> bool:
    """
    Authenticates and initializes the Google Earth Engine API.
    """
    ee_project = project_id or os.getenv("EE_PROJECT_ID")

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
    initialize_earth_engine()