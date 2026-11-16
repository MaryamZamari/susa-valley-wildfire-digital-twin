import ee
import geemap
import contextily as ctx
import matplotlib.pyplot as plt
from src.config import OUTPUT_TRANSIT_MAP

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

#geographic importance and complexity
def render_transit_map(burn_scar_m, highways_m, railways_m):
    """Renders the dark-mode transit and burn scar map."""
    fig, ax = plt.subplots(figsize=(12, 8), facecolor="#121212")
    ax.set_facecolor("#121212")

    # Plot layers
    burn_scar_m.plot(
        ax=ax, color="#FF3366", alpha=0.5, edgecolor="#FFFFFF", linewidth=0.8, label="Burn Scar"
    )
    highways_m.plot(
        ax=ax, color="#00F0FF", linewidth=1.5, label="A32 Highway"
    )
    railways_m.plot(
        ax=ax, color="#FFFFFF", linewidth=1.0, linestyle="--", label="Railway"
    )

    # Add CartoDB Dark Matter basemap tiles
    ctx.add_basemap(
        ax,
        source=ctx.providers.CartoDB.DarkMatter,
        crs=burn_scar_m.crs,
        zoom=12,
    )

    # Formatting
    ax.set_title(
        "Susa Valley International Transit Corridor & Wildfire AOI",
        color="white",
        fontsize=14,
        pad=15,
        weight="bold",
    )
    ax.axis("off")

    # Save output
    plt.savefig(
        OUTPUT_TRANSIT_MAP,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    print(f"Map successfully compiled and saved to {OUTPUT_TRANSIT_MAP}!")


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