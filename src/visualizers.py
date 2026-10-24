# src/visualizers.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_dnbr_histogram(df: pd.DataFrame):
    """Plots the dNBR burn severity histogram with USGS thresholds."""
    plt.figure(figsize=(10, 5))
    sns.histplot(df['dnbr'], bins=50, kde=True, color='firebrick')

    plt.axvline(x=0.1, color='gray', linestyle='--', label='Low Severity (0.1)')
    plt.axvline(x=0.27, color='orange', linestyle='--', label='Moderate Severity (0.27)')
    plt.axvline(x=0.44, color='red', linestyle='--', label='High Severity (0.44)')

    plt.title('EMSR253 Susa Valley - dNBR Burn Severity Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('dNBR (Differenced Normalized Burn Ratio)', fontsize=12)
    plt.ylabel('Pixel Count', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_ndvi_scatterplot(df: pd.DataFrame):
    """Plots pre-fire vs post-fire NDVI vegetation health collapse."""
    plt.figure(figsize=(7, 7))
    sns.scatterplot(
        data=df,
        x='pre_ndvi',
        y='post_ndvi',
        alpha=0.4,
        color='forestgreen',
        edgecolor=None,
        s=15
    )

    plt.plot([-0.2, 0.8], [-0.2, 0.8], color='black', linestyle='--', label='1:1 Line (No Change)')

    plt.title('Vegetation Health Collapse: Pre vs. Post-Fire NDVI', fontsize=14, fontweight='bold')
    plt.xlabel('Pre-Fire NDVI (September 2017)', fontsize=12)
    plt.ylabel('Post-Fire NDVI (October/November 2017)', fontsize=12)
    plt.xlim(-0.2, 0.8)
    plt.ylim(-0.2, 0.8)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()