import rasterio
import numpy as np

DEM_PATH = "data/terrain/output_SRTMGL3.tif"

with rasterio.open(DEM_PATH) as src:

    dem = src.read(1)

    valid = dem[dem != 0]

    print("Total pixels:", dem.size)
    print("NoData pixels:", np.sum(dem == 0))
    print("Valid pixels:", len(valid))

    print("\nElevation:")
    print("Minimum:", valid.min())
    print("Maximum:", valid.max())
    print("Mean:", valid.mean())