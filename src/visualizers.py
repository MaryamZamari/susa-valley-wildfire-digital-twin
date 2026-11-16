import matplotlib

matplotlib.use('Agg')  # Force non-interactive backend to prevent C-level GUI crashes

import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image, display


def plot_dnbr_histogram(df, output_path="temp_dnbr_hist.png"):
    """
    Generates and safely renders the dNBR burn severity distribution histogram
    by saving to disk and displaying as an image, preventing kernel crashes.
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df['dnbr'], bins=50, kde=True, color='firebrick', ax=ax)
    ax.set_title('dNBR Burn Severity Distribution', fontsize=12, fontweight='bold')
    ax.set_xlabel('dNBR Value', fontsize=10)
    ax.set_ylabel('Pixel Count', fontsize=10)
    plt.tight_layout()

    # Save locally to bypass live IPython stream socket crashes
    plt.savefig(output_path, dpi=150)
    plt.close(fig)

    # Display safely
    display(Image(output_path))


def plot_ndvi_scatterplot(df, output_path="temp_ndvi_scatter.png"):
    """
    Generates and safely renders the Pre vs. Post-Fire NDVI scatterplot
    by saving to disk and displaying as an image, preventing kernel crashes.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=df, x='pre_ndvi', y='post_ndvi', alpha=0.5, color='teal', ax=ax)
    ax.set_title('Pre vs. Post-Fire NDVI', fontsize=12, fontweight='bold')
    ax.set_xlabel('Pre-Fire NDVI', fontsize=10)
    ax.set_ylabel('Post-Fire NDVI', fontsize=10)

    # Add a 1:1 reference line for visual baseline comparison
    ax.plot([0, 1], [0, 1], transform=ax.transAxes, color='gray', linestyle='--', linewidth=1)

    plt.tight_layout()

    # Save locally to bypass live IPython stream socket crashes
    plt.savefig(output_path, dpi=150)
    plt.close(fig)

    # Display safely
    display(Image(output_path))