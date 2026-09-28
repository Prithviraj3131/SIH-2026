import geopandas as gpd

file_path = "data/processed/pune_landslides.gpkg"

landslides = gpd.read_file(
    file_path,
    layer="landslides"
)

print("Total Pune landslides:", len(landslides))

print("\nColumns:")
print(landslides.columns.tolist())

print("\nCRS:")
print(landslides.crs)

print("\nFirst 10 records:")
print(
    landslides[
        [
            "source_state",
            "source_district",
            "district",
            "state",
            "Latitude",
            "Longitude",
            "Material Involved",
            "Movement Type"
        ]
    ].head(10).to_string(index=False)
)