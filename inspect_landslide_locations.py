import pandas as pd
import geopandas as gpd


# -------------------------------------------------
# File path
# -------------------------------------------------

file_path = "data/landslide/landslide_inventory_ML_training.xlsx"


# -------------------------------------------------
# Load landslide data
# -------------------------------------------------

landslides = pd.read_excel(file_path)

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

osm_file = "data/osm/western-zone.gpkg"

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
)


# -------------------------------------------------
# Results
# -------------------------------------------------

print("\n--------------------------------")
print("LANDSLIDES INSIDE PUNE")
print("--------------------------------")

print(
    "Historical landslides in Pune:",
    len(pune_landslides)
)


print("\nFirst 20 records:")

print(
    pune_landslides[
        [
            "State",
            "District",
            "Slide_Name",
            "Latitude",
            "Longitude",
            "Material Involved",
            "Movement Type"
        ]
    ]
    .head(20)
    .to_string(index=False)
)