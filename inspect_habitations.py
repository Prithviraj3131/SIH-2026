import geopandas as gpd
import pandas as pd

PATH = "data/processed/pune_landslide_training_data_v3.gpkg"

data = gpd.read_file(PATH)

print("Total samples:", len(data))


# -------------------------------------------------
# Feature statistics by class
# -------------------------------------------------

print("\nFEATURE STATISTICS BY LABEL")
print("---------------------------")

print(
    data.groupby("label")[
        [
            "slope_degrees",
            "elevation_m",
            "rainfall_2024_mm"
        ]
    ].agg(
        ["min", "mean", "max"]
    )
)


# -------------------------------------------------
# Check repaired zero slopes
# -------------------------------------------------

zero_slope = data[data["slope_degrees"] == 0]

print("\nZero-slope samples:", len(zero_slope))

print("\nZero-slope samples by label:")
print(zero_slope["label"].value_counts())


# -------------------------------------------------
# Check duplicate coordinates
# -------------------------------------------------

data["x"] = data.geometry.x
data["y"] = data.geometry.y

duplicate_count = data.duplicated(
    subset=["x", "y"]
).sum()

print("\nDuplicate coordinate records:", duplicate_count)

print("\nDuplicate coordinates:")
print(
    data[
        data.duplicated(
            subset=["x", "y"],
            keep=False
        )
    ][
        [
            "x",
            "y",
            "slope_degrees",
            "elevation_m",
            "rainfall_2024_mm",
            "label"
        ]
    ].sort_values(["x", "y"]).head(30)
)


# -------------------------------------------------
# Check class balance
# -------------------------------------------------

print("\nCLASS DISTRIBUTION")
print("------------------")

print(data["label"].value_counts())

print("\nClass percentages:")

print(
    data["label"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)