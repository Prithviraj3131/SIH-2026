import geopandas as gpd


INPUT_PATH = "data/processed/pune_landslide_training_data_v3.gpkg"
OUTPUT_PATH = "data/processed/pune_landslide_ml_ready.gpkg"


# -------------------------------------------------
# Load data
# -------------------------------------------------

data = gpd.read_file(INPUT_PATH)

print("Original samples:", len(data))


# -------------------------------------------------
# Remove artificial zero-slope samples
# -------------------------------------------------

zero_slope = data["slope_degrees"] == 0

print("Zero-slope samples removed:", zero_slope.sum())

data = data[~zero_slope].copy()


# -------------------------------------------------
# Remove duplicate coordinates
# -------------------------------------------------

data["x"] = data.geometry.x
data["y"] = data.geometry.y

duplicates = data.duplicated(
    subset=["x", "y"],
    keep="first"
)

print("Duplicate coordinate records removed:", duplicates.sum())

data = data[~duplicates].copy()


# -------------------------------------------------
# Remove helper columns
# -------------------------------------------------

data = data.drop(
    columns=["x", "y"]
)


# -------------------------------------------------
# Check missing values
# -------------------------------------------------

print("\nMissing values:")

print(
    data[
        [
            "slope_degrees",
            "elevation_m",
            "rainfall_2024_mm"
        ]
    ].isna().sum()
)


# -------------------------------------------------
# Final class distribution
# -------------------------------------------------

print("\nFinal class distribution:")

print(data["label"].value_counts())


# -------------------------------------------------
# Save
# -------------------------------------------------

data.to_file(
    OUTPUT_PATH,
    driver="GPKG"
)

print("\nML-ready dataset saved to:")
print(OUTPUT_PATH)

print("\nFinal samples:", len(data))