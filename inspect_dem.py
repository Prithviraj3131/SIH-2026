import geopandas as gpd

PATH = "data/processed/pune_landslide_training_data_v2.gpkg"

data = gpd.read_file(PATH)

missing = data[data["slope_degrees"].isna()]

print("Total samples:", len(data))

print("\nMissing slope samples:", len(missing))

print("\nMissing slope by label:")
print(missing["label"].value_counts())

print("\nMissing slope records:")
print(
    missing[
        [
            "slope_degrees",
            "elevation_m",
            "rainfall_2024_mm",
            "label",
            "geometry"
        ]
    ]
)