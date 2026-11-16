import ee
import gpd
import geopandas as gpd
from shapely.geometry import shape

import geopandas as gpd
from shapely.geometry import shape


def prepare_transit_data(burn_scar, highways, railways):
    """Reprojects all spatial layers to Web Mercator for basemap alignment,
    handling both GeoDataFrames and raw geometry inputs safely."""

    if not isinstance(burn_scar, gpd.GeoDataFrame):
        if hasattr(burn_scar, 'getInfo'):  # It's an ee.Geometry
            geom_json = burn_scar.getInfo()
            # Wrap it into a GeoJSON Feature dictionary so from_features() accepts it
            feature = {
                "type": "Feature",
                "geometry": geom_json,
                "properties": {}
            }
            burn_scar = gpd.GeoDataFrame.from_features([feature], crs="EPSG:4326")
        else:  # Assume it's a raw Shapely geometry
            burn_scar = gpd.GeoDataFrame(geometry=[burn_scar], crs="EPSG:4326")

    # Re-project to Web Mercator
    burn_scar_m = burn_scar.to_crs(epsg=3857)
    highways_m = highways.to_crs(epsg=3857)
    railways_m = railways.to_crs(epsg=3857)

    return burn_scar_m, highways_m, railways_m

def calculate_ndvi(image: ee.Image) -> ee.Image:
    """
    Computes the Normalized Difference Vegetation Index (NDVI) for a Sentinel-2 image.
    Formula: (B8 - B4) / (B8 + B4)
    """
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    return image.addBands(ndvi)


def calculate_nbr(image: ee.Image) -> ee.Image:
    """
    Computes the Normalized Burn Ratio (NBR) for a Sentinel-2 image.
    Formula: (B8 - B12) / (B8 + B12)
    """
    nbr = image.normalizedDifference(['B8', 'B12']).rename('NBR')
    return image.addBands(nbr)


def calculate_dnbr(pre_fire_image: ee.Image, post_fire_image: ee.Image) -> ee.Image:
    """
    Computes the difference NBR (dNBR) between pre-fire and post-fire imagery.
    Formula: NBR_pre - NBR_post
    """
    pre_nbr = calculate_nbr(pre_fire_image).select('NBR')
    post_nbr = calculate_nbr(post_fire_image).select('NBR')

    dnbr = pre_nbr.subtract(post_nbr).rename('dNBR')
    return dnbr


def extract_burnt_area(dnbr_image: ee.Image, threshold: float = 0.27) -> ee.Image:
    """
    Extracts a binary mask of the burnt area based on a dNBR threshold
    (standard USGS threshold for moderate-high burn severity ~0.27).
    """
    burn_mask = dnbr_image.gte(threshold).rename('burn_mask')
    return burn_mask


if __name__ == "__main__":
    from src.config import initialize_earth_engine
    from src.data_loaders import get_susa_valley_aoi, get_sentinel2_collection

    initialize_earth_engine()
    aoi = get_susa_valley_aoi()

    # Example test using a specific date window around the Susa Valley event
    collection = get_sentinel2_collection(aoi, "2022-07-01", "2022-09-30")
    print(f"[INFO] Processors module loaded successfully. Ready to process {collection.size().getInfo()} images.")