import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from .data import CITIES

def plot_route_globe(route, distance_km, save_path=None):
    fig = plt.figure(figsize=(15, 15))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    ax.stock_img()
    ax.gridlines()

    lons = [c[1] for c in CITIES]
    lats = [c for c in CITIES]
    names = [c[2] for c in CITIES]

    for i in range(len(route)-1):
        s, e = route[i], route[i+1]
        ax.plot([lons[s], lons[e]], [lats[s], lats[e]], color='red', linewidth=2, marker='o',
                transform=ccrs.Geodetic())

    pos_in_route = {city: idx+1 for idx, city in enumerate(route)}
    for i, (lat, lon, name) in enumerate(CITIES):
        label = f"{name} ({pos_in_route.get(i, '?')})"
        ax.text(lon + 2, lat, label, transform=ccrs.Geodetic(), bbox=dict(facecolor='white', alpha=0.7))

    plt.title(f"Optimal route (distance: {distance_km:.2f} km)")
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()
        plt.close(fig)
