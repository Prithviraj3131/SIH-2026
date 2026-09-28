import rasterio
import numpy as np
from rasterio.warp import calculate_default_transform, reproject
from rasterio.enums import Resampling


DEM_PATH = "data/terrain/output_SRTMGL3.tif"
OUTPUT_PATH = "data/terrain/pune_slope_90m.tif"

TARGET_CRS = "EPSG:32643"


# -------------------------------------------------
# Read and reproject DEM
# -------------------------------------------------

with rasterio.open(DEM_PATH) as src:

    print("Original DEM CRS:", src.crs)
    print("Original resolution:", src.res)

    dem = src.read(1).astype("float32")

    # Original NoData is 0
    nodata_mask = dem == 0

    # Convert NoData to NaN temporarily
    dem[nodata_mask] = np.nan

    transform, width, height = calculate_default_transform(
        src.crs,
        TARGET_CRS,
        src.width,
        src.height,
        *src.bounds
    )

    projected_dem = np.empty(
        (height, width),
        dtype="float32"
    )

    reproject(
        source=dem,
        destination=projected_dem,
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=transform,
        dst_crs=TARGET_CRS,
        src_nodata=np.nan,
        dst_nodata=np.nan,
        resampling=Resampling.bilinear
    )


# -------------------------------------------------
# Handle NoData before calculating slope
# -------------------------------------------------

valid_values = projected_dem[
    ~np.isnan(projected_dem)
]

mean_elevation = np.mean(valid_values)

print("\nValid elevation pixels:", len(valid_values))
print("Mean elevation:", mean_elevation)

# Temporarily fill NoData cells
# so they don't contaminate np.gradient()
dem_for_slope = projected_dem.copy()

dem_for_slope[np.isnan(dem_for_slope)] = mean_elevation


# -------------------------------------------------
# Calculate slope
# -------------------------------------------------

pixel_size_x = transform.a
pixel_size_y = abs(transform.e)

print("\nProjected pixel size:")
print("Width:", pixel_size_x, "meters")
print("Height:", pixel_size_y, "meters")


gradient_y, gradient_x = np.gradient(
    dem_for_slope,
    pixel_size_y,
    pixel_size_x
)


slope_radians = np.arctan(
    np.sqrt(
        gradient_x ** 2 +
        gradient_y ** 2
    )
)


slope_degrees = np.degrees(slope_radians)


# -------------------------------------------------
# Restore NoData areas
# -------------------------------------------------

slope_degrees[np.isnan(projected_dem)] = -9999


# -------------------------------------------------
# Save slope raster
# -------------------------------------------------

profile = {
    "driver": "GTiff",
    "height": height,
    "width": width,
    "count": 1,
    "dtype": "float32",
    "crs": TARGET_CRS,
    "transform": transform,
    "nodata": -9999
}


with rasterio.open(
    OUTPUT_PATH,
    "w",
    **profile
) as dst:

    dst.write(
        slope_degrees.astype("float32"),
        1
    )


# -------------------------------------------------
# Statistics
# -------------------------------------------------

valid_slope = slope_degrees[
    slope_degrees != -9999
]

print("\nSLOPE RASTER CREATED")
print("--------------------")

print(
    "Minimum slope:",
    np.min(valid_slope),
    "degrees"
)

print(
    "Maximum slope:",
    np.max(valid_slope),
    "degrees"
)

print(
    "Mean slope:",
    np.mean(valid_slope),
    "degrees"
)

print("\nSaved to:")
print(OUTPUT_PATH)