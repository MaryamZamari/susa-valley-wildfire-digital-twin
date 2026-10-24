import ee
import geemap


def create_base_map(center: list = [45.133, 7.05], zoom: int = 11) -> geemap.Map:
    """
    Initializes an interactive geemap Map centered over the Susa Valley study area.

    Args:
        center (list): [latitude, longitude] for map center.
        zoom (int): Initial zoom level.

    Returns:
        geemap.Map: Interactive map object.
    """
    Map = geemap.Map(center=center, zoom=zoom)
    Map.add_basemap('HYBRID')  # Add a high-resolution satellite basemap for reference
    return Map


def add_sentinel2_layer(
        Map: geemap.Map,
        image: ee.Image,
        name: str = "Sentinel-2 Image",
        vis_params: dict = None
) -> None:
    """
    Adds a Sentinel-2 image layer to the map.
    """
    if vis_params is None:
        vis_params = {
            'bands': ['B4', 'B3', 'B2'],  # True color RGB
            'min': 0,
            'max': 3000,
            'gamma': 1.4
        }
    Map.addLayer(image, vis_params, name)


def add_index_layer(
        Map: geemap.Map,
        image: ee.Image,
        band_name: str,
        palette: list,
        min_val: float,
        max_val: float,
        layer_name: str
) -> None:
    """
    Adds a styled raster index layer (like NDVI or dNBR) to the map with custom color palettes.
    """
    vis_params = {
        'min': min_val,
        'max': max_val,
        'palette': palette
    }
    Map.addLayer(image.select(band_name), vis_params, layer_name)


if __name__ == "__main__":
    from src.config import initialize_earth_engine
    from src.data_loaders import get_susa_valley_aoi, get_sentinel2_collection
    from src.processors import calculate_ndvi, calculate_dnbr

    initialize_earth_engine()

    # Quick sanity check test
    Map = create_base_map()
    print("[INFO] Map builder initialized successfully. Ready for layer rendering.")