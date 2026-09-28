import geopandas as gpd
import rasterio
import numpy as np
import joblib

from rasterio.mask import mask
from rasterio.transform import xy


# -------------------------------------------------
# Paths
# -------------------------------------------------

MODEL_PATH = "ml/landslide_model.pkl"

DEM_PATH = "data/terrain/output_SRTMGL3.tif"
SLOPE_PATH = "data/terrain/pune_slope_90m.tif"
RAINFALL_PATH = "data/rainfall/chirps-v3.0.2024.tif"

OSM_PATH = "data/osm/western-zone.gpkg"

OUTPUT_PATH = "data/processed/pune_landslide_susceptibility.tif"


# -------------------------------------------------
# Load model
# -------------------------------------------------

print("Loading Random Forest model...")

model = joblib.load(MODEL_PATH)

print("Model loaded.")


# -------------------------------------------------
# Load Pune boundary
# -------------------------------------------------

admin = gpd.read_file(
    OSM_PATH,
    layer="gis_osm_adminareas_a_free"
)

pune = admin[
    (admin["fclass"] == "admin_level5") &
    (admin["name"].str.lower() == "pune")
].copy()

if pune.empty:
    raise ValueError("Pune district boundary not found.")

print("Pune boundary loaded.")


# -------------------------------------------------
# Use slope raster as prediction grid
# -------------------------------------------------

with rasterio.open(SLOPE_PATH) as slope_src:

    print("\nSlope raster:")
    print("Width:", slope_src.width)
    print("Height:", slope_src.height)
    print("CRS:", slope_src.crs)
    print("Resolution:", slope_src.res)

    slope = slope_src.read(1)

    profile = slope_src.profile.copy()

    transform = slope_src.transform
    width = slope_src.width
    height = slope_src.height
    raster_crs = slope_src.crs


# -------------------------------------------------
# Convert Pune boundary to raster CRS
# -------------------------------------------------

pune = pune.to_crs(raster_crs)


# -------------------------------------------------
# Create Pune mask
# -------------------------------------------------

from rasterio.features import geometry_mask

pune_mask = geometry_mask(
    pune.geometry,
    out_shape=(height, width),
    transform=transform,
    invert=True
)


# -------------------------------------------------
# Read elevation
# -------------------------------------------------

with rasterio.open(DEM_PATH) as src:

    elevation = src.read(
        1,
        out_shape=(height, width),
        resampling=rasterio.enums.Resampling.bilinear
    )


# -------------------------------------------------
# Read rainfall
# -------------------------------------------------

with rasterio.open(RAINFALL_PATH) as src:

    rainfall = src.read(
        1,
        out_shape=(height, width),
        resampling=rasterio.enums.Resampling.bilinear
    )


# -------------------------------------------------
# Prepare valid pixels
# -------------------------------------------------

valid = (
    pune_mask &
    (slope != -9999) &
    (elevation != 0) &
    (rainfall > -9000)
)

rows, cols = np.where(valid)

print("\nValid prediction pixels:", len(rows))


# -------------------------------------------------
# Extract feature values
# -------------------------------------------------

slope_values = slope[rows, cols]
elevation_values = elevation[rows, cols]
rainfall_values = rainfall[rows, cols]


X = np.column_stack(
    [
        slope_values,
        elevation_values,
        rainfall_values
    ]
)


# -------------------------------------------------
# Predict landslide probability
# -------------------------------------------------

print("\nPredicting susceptibility...")

probability = model.predict_proba(X)[:, 1]


# -------------------------------------------------
# Create output raster
# -------------------------------------------------

susceptibility = np.full(
    (height, width),
    -9999,
    dtype="float32"
)

susceptibility[rows, cols] = probability


# -------------------------------------------------
# Save raster
# -------------------------------------------------

profile.update(
    driver="GTiff",
    dtype="float32",
    count=1,
    nodata=-9999
)

with rasterio.open(
    OUTPUT_PATH,
    "w",
    **profile
) as dst:

    dst.write(
        susceptibility,
        1
    )


# -------------------------------------------------
# Statistics
# -------------------------------------------------

valid_probability = probability[
    np.isfinite(probability)
]

print("\nSUSCEPTIBILITY MAP CREATED")
print("--------------------------")

print("Minimum probability:",
      valid_probability.min())

print("Maximum probability:",
      valid_probability.max())

print("Mean probability:",
      valid_probability.mean())

print("\nSaved to:")
print(OUTPUT_PATH)