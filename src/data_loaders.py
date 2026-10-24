import os
import ee
import geemap
from src.config import (
    EMSR253_COORDS_BB,
    PRE_FIRE_START,
    PRE_FIRE_END,
    POST_FIRE_START,
    POST_FIRE_END,
    initialize_earth_engine
)


def get_susa_valley_aoi() -> ee.Geometry:
    """
    Loads the official Copernicus CEMS irregular boundary GeoJSON
    from the resources folder and returns it as an Earth Engine Geometry.
    Falls back to the bounding box if the file is not found.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    # Update filename here if your exported file has a different name!
    geojson_path = os.path.join(project_root, "resources", "EMSR253_susa_del_2017_converted.geojson")

    if os.path.exists(geojson_path):
        try:
            cems_feature_collection = geemap.geojson_to_ee(geojson_path)
            print(f"[INFO] Successfully loaded official CEMS irregular boundary from: {geojson_path}")
            return cems_feature_collection.geometry()
        except Exception as e:
            print(f"[WARNING] Could not parse GeoJSON into Earth Engine: {e}. Falling back to bounding box.")
            return ee.Geometry.Polygon(EMSR253_COORDS_BB)
    else:
        print(f"[WARNING] CEMS GeoJSON file not found at {geojson_path}. Falling back to bounding box.")
        return ee.Geometry.Polygon(EMSR253_COORDS_BB)


def get_bounding_box_extent() -> ee.Geometry:
    """
    Returns the broader rectangular bounding box polygon (EMSR253_COORDS_BB)
    useful for map framing and broader spatial extents.
    """
    return ee.Geometry.Polygon(EMSR253_COORDS_BB)


def get_sentinel2_collection(
        aoi: ee.Geometry,
        start_date: str,
        end_date: str,
        max_cloud_cover: float = 20.0
) -> ee.ImageCollection:
    """
    Retrieves cloud-filtered Sentinel-2 imagery (COPERNICUS/S2_SR_HARMONIZED)
    for the given AOI and date range.
    """
    return (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', max_cloud_cover))
    )


if __name__ == "__main__":
    initialize_earth_engine()
    aoi = get_susa_valley_aoi()
    bbox = get_bounding_box_extent()

    # Test loading collection with the correct 2017 pre-fire window
    collection = get_sentinel2_collection(aoi, PRE_FIRE_START, PRE_FIRE_END)
    print(f"[INFO] Sentinel-2 collection loaded successfully. Image count: {collection.size().getInfo()}")