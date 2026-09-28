import geopandas as gpd
import rasterio
import numpy as np

LANDSLIDES_PATH = "data/processed/pune_landslides_features.gpkg"
RAINFALL_PATH = "data/rainfall/chirps-v3.0.2024.tif"
OUTPUT_PATH = "data/processed/pune_landslides_ml_features.gpkg"


# -------------------------------------------------
# Load landslides
# -------------------------------------------------

landslides = gpd.read_file(LANDSLIDES_PATH)

print("Number of landslides:", len(landslides))
print("Landslide CRS:", landslides.crs)


# -------------------------------------------------
# Open rainfall raster
# -------------------------------------------------

with rasterio.open(RAINFALL_PATH) as src:

    print("\nRainfall CRS:", src.crs)
    print("Rainfall resolution:", src.res)

    # Make sure points use the same CRS as rainfall
    landslides_rainfall_crs = landslides.to_crs(src.crs)

    # Get coordinates of every landslide
    coordinates = [
        (point.x, point.y)
        for point in landslides_rainfall_crs.geometry
    ]

    # Extract rainfall values
    values = []

    for value in src.sample(coordinates):
        rainfall = float(value[0])

        # CHIRPS missing-data value
        if rainfall <= -9000:
            rainfall = np.nan

        values.append(rainfall)


# -------------------------------------------------
# Add rainfall feature
# -------------------------------------------------

landslides["rainfall_2024_mm"] = values


# -------------------------------------------------
# Display results
# -------------------------------------------------

print("\nRainfall extraction complete")

print("Minimum rainfall:",
      landslides["rainfall_2024_mm"].min())

print("Maximum rainfall:",
      landslides["rainfall_2024_mm"].max())

print("Mean rainfall:",
      landslides["rainfall_2024_mm"].mean())

print("Missing rainfall values:",
      landslides["rainfall_2024_mm"].isna().sum())


print("\nFirst 10 records:")
print(
    landslides[
        [
            "source_state",
            "source_district",
            "slope_degrees",
            "elevation_m",
            "rainfall_2024_mm"
        ]
    ].head(10)
)


# -------------------------------------------------
# Save
# -------------------------------------------------

landslides.to_file(
    OUTPUT_PATH,
    driver="GPKG"
)

print("\nSaved to:")
print(OUTPUT_PATH)