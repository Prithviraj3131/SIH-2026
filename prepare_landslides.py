import pandas as pd
import geopandas as gpd
import os


# -------------------------------------------------
# File paths
# -------------------------------------------------

input_file = "data/landslide/landslide_inventory_ML_training.xlsx"
osm_file = "data/osm/western-zone.gpkg"

output_folder = "data/processed"

os.makedirs(output_folder, exist_ok=True)


# -------------------------------------------------
# Load landslide inventory
# -------------------------------------------------

landslides = pd.read_excel(input_file)

print("Total landslide records:", len(landslides))


# -------------------------------------------------
# Remove records without coordinates
# -------------------------------------------------

landslides = landslides.dropna(
    subset=["Latitude", "Longitude"]
).copy()

print("Records with coordinates:", len(landslides))


# -------------------------------------------------
# Convert to GeoDataFrame
# -------------------------------------------------

landslide_points = gpd.GeoDataFrame(
    landslides,
    geometry=gpd.points_from_xy(
        landslides["Longitude"],
        landslides["Latitude"]
    ),
    crs="EPSG:4326"
)


# -------------------------------------------------
# Load district boundaries
# -------------------------------------------------

districts = gpd.read_file(
    osm_file,
    layer="gis_osm_adminareas_a_free"
)

districts = districts[
    districts["fclass"] == "admin_level5"
].copy()


# -------------------------------------------------
# Select Pune
# -------------------------------------------------

pune = districts[
    districts["name"].str.lower() == "pune"
].copy()


# -------------------------------------------------
# Match CRS
# -------------------------------------------------

landslide_points = landslide_points.to_crs(
    pune.crs
)


# -------------------------------------------------
# Find landslides inside Pune
# -------------------------------------------------

pune_landslides = gpd.sjoin(
    landslide_points,
    pune[["name", "geometry"]],
    how="inner",
    predicate="within"
).copy()


# -------------------------------------------------
# Rename original source fields
# -------------------------------------------------

pune_landslides = pune_landslides.rename(
    columns={
        "State": "source_state",
        "District": "source_district"
    }
)


# -------------------------------------------------
# Add project fields
# -------------------------------------------------

pune_landslides["district"] = "Pune"
pune_landslides["state"] = "Maharashtra"
# -------------------------------------------------
# Save
# -------------------------------------------------

output_file = os.path.join(
    output_folder,
    "pune_landslides.gpkg"
)

pune_landslides.to_file(
    output_file,
    layer="landslides",
    driver="GPKG"
)


# -------------------------------------------------
# Summary
# -------------------------------------------------

print("\n--------------------------------")
print("PUNE LANDSLIDE DATASET CREATED")
print("--------------------------------")

print(
    "Historical landslides:",
    len(pune_landslides)
)

print("\nSaved to:")
print(output_file)