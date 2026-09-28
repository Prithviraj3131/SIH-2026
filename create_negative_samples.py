import geopandas as gpd
import rasterio
import numpy as np
import pandas as pd
from shapely.geometry import Point


# -------------------------------------------------
# Paths
# -------------------------------------------------

LANDSLIDES_PATH = "data/processed/pune_landslides.gpkg"
OSM_PATH = "data/osm/western-zone.gpkg"

SLOPE_PATH = "data/terrain/pune_slope_90m.tif"
ELEVATION_PATH = "data/terrain/output_SRTMGL3.tif"
RAINFALL_PATH = "data/rainfall/chirps-v3.0.2024.tif"

OUTPUT_PATH = "data/processed/pune_landslide_training_data_v2.gpkg"


# -------------------------------------------------
# Settings
# -------------------------------------------------

NEGATIVE_RATIO = 2
BUFFER_DISTANCE = 500

np.random.seed(42)


# -------------------------------------------------
# Load historical landslides
# -------------------------------------------------

landslides = gpd.read_file(
    LANDSLIDES_PATH,
    layer="landslides"
)

print("Historical landslides:", len(landslides))


# -------------------------------------------------
# Load Pune district boundary
# -------------------------------------------------

admin = gpd.read_file(
    OSM_PATH,
    layer="gis_osm_adminareas_a_free"
)

pune_boundary = admin[
    (admin["fclass"] == "admin_level5") &
    (admin["name"].str.lower() == "pune")
].copy()

if pune_boundary.empty:
    raise ValueError("Pune district boundary not found.")

print("Pune district boundary found.")


# -------------------------------------------------
# Convert to metric CRS
# -------------------------------------------------

metric_crs = "EPSG:32643"

pune_boundary = pune_boundary.to_crs(metric_crs)
landslides_metric = landslides.to_crs(metric_crs)


# -------------------------------------------------
# Create exclusion zone
# -------------------------------------------------

print("\nCreating 500 m exclusion zones...")

exclusion_geometry = (
    landslides_metric.geometry
    .buffer(BUFFER_DISTANCE)
    .union_all()
)


# -------------------------------------------------
# Generate negative samples
# -------------------------------------------------

target_negative_count = len(landslides) * NEGATIVE_RATIO

print("Target negative samples:", target_negative_count)

district_polygon = pune_boundary.geometry.union_all()

minx, miny, maxx, maxy = district_polygon.bounds

negative_points = []

while len(negative_points) < target_negative_count:

    x = np.random.uniform(minx, maxx)
    y = np.random.uniform(miny, maxy)

    point = Point(x, y)

    if not district_polygon.contains(point):
        continue

    if exclusion_geometry.contains(point):
        continue

    negative_points.append(point)


negative_samples = gpd.GeoDataFrame(
    {
        "label": [0] * len(negative_points)
    },
    geometry=negative_points,
    crs=metric_crs
)

print("Negative samples generated:", len(negative_samples))


# -------------------------------------------------
# Raster extraction function
# -------------------------------------------------

def extract_raster_values(points, raster_path):

    with rasterio.open(raster_path) as src:

        points_raster_crs = points.to_crs(src.crs)

        coordinates = [
            (point.x, point.y)
            for point in points_raster_crs.geometry
        ]

        values = []

        for value in src.sample(coordinates):

            number = float(value[0])

            if number <= -9000 or number == 0:
                number = np.nan

            values.append(number)

    return values


# -------------------------------------------------
# Extract negative sample features
# -------------------------------------------------

print("\nExtracting slope...")

negative_samples["slope_degrees"] = extract_raster_values(
    negative_samples,
    SLOPE_PATH
)


print("Extracting elevation...")

negative_samples["elevation_m"] = extract_raster_values(
    negative_samples,
    ELEVATION_PATH
)


print("Extracting rainfall...")

negative_samples["rainfall_2024_mm"] = extract_raster_values(
    negative_samples,
    RAINFALL_PATH
)


# -------------------------------------------------
# Prepare positive samples
# -------------------------------------------------

print("\nPreparing positive samples...")

positive_samples = landslides.copy()

positive_samples = positive_samples.to_crs(metric_crs)

# Extract terrain features again from the new rasters

print("Extracting positive sample slope...")

positive_samples["slope_degrees"] = extract_raster_values(
    positive_samples,
    SLOPE_PATH
)

print("Extracting positive sample elevation...")

positive_samples["elevation_m"] = extract_raster_values(
    positive_samples,
    ELEVATION_PATH
)

print("Extracting positive sample rainfall...")

positive_samples["rainfall_2024_mm"] = extract_raster_values(
    positive_samples,
    RAINFALL_PATH
)

positive_samples["label"] = 1

print("Positive samples prepared:", len(positive_samples))


# -------------------------------------------------
# Keep only required columns
# -------------------------------------------------

positive_samples = positive_samples[
    [
        "slope_degrees",
        "elevation_m",
        "rainfall_2024_mm",
        "geometry",
        "label"
    ]
]

negative_samples = negative_samples[
    [
        "slope_degrees",
        "elevation_m",
        "rainfall_2024_mm",
        "geometry",
        "label"
    ]
]


# -------------------------------------------------
# Combine
# -------------------------------------------------

print("\nCombining positive and negative samples...")

training_data = gpd.GeoDataFrame(
    pd.concat(
        [
            positive_samples,
            negative_samples
        ],
        ignore_index=True
    ),
    crs=metric_crs
)

print("Datasets combined successfully.")
print("Total samples:", len(training_data))


# -------------------------------------------------
# Check missing values
# -------------------------------------------------

print("\nMissing values:")

print(
    training_data[
        [
            "slope_degrees",
            "elevation_m",
            "rainfall_2024_mm"
        ]
    ].isna().sum()
)


# -------------------------------------------------
# Save
# -------------------------------------------------

print("\nSaving training dataset...")

training_data.to_file(
    OUTPUT_PATH,
    driver="GPKG"
)


# -------------------------------------------------
# Final information
# -------------------------------------------------

print("\nTRAINING DATA CREATED")
print("---------------------")

print(
    "Positive samples:",
    (training_data["label"] == 1).sum()
)

print(
    "Negative samples:",
    (training_data["label"] == 0).sum()
)

print(
    "Total samples:",
    len(training_data)
)

print("\nFeatures:")

print(
    [
        "slope_degrees",
        "elevation_m",
        "rainfall_2024_mm"
    ]
)

print("\nSaved to:")

print(OUTPUT_PATH)