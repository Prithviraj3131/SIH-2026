import geopandas as gpd
import os

# -------------------------------------------------
# File paths
# -------------------------------------------------

osm_file = "data/osm/western-zone.gpkg"
output_folder = "data/processed"

os.makedirs(output_folder, exist_ok=True)


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

if pune.empty:
    print("Pune district was not found.")
    exit()

print("Pune district found.")


# -------------------------------------------------
# Load habitation/place points
# -------------------------------------------------

places = gpd.read_file(
    osm_file,
    layer="gis_osm_places_free"
)

print("Total OSM places:", len(places))


# -------------------------------------------------
# Keep actual settlement types
# -------------------------------------------------

habitation_types = [
    "village",
    "hamlet",
    "town",
    "city"
]

places = places[
    places["fclass"].isin(habitation_types)
].copy()

print("Settlement points:", len(places))


# -------------------------------------------------
# Match coordinate systems
# -------------------------------------------------

places = places.to_crs(pune.crs)


# -------------------------------------------------
# Find settlements inside Pune
# -------------------------------------------------

pune_habitations = gpd.sjoin(
    places,
    pune[["name", "geometry"]],
    how="inner",
    predicate="within"
).copy()


# -------------------------------------------------
# Rename columns
# -------------------------------------------------

pune_habitations = pune_habitations.rename(
    columns={
        "name_left": "habitation_name",
        "fclass": "habitation_type",
        "population": "population"
    }
)


# -------------------------------------------------
# Add district and state
# -------------------------------------------------

pune_habitations["district"] = "Pune"
pune_habitations["state"] = "Maharashtra"


# -------------------------------------------------
# Keep only required columns
# -------------------------------------------------

pune_habitations = pune_habitations[
    [
        "osm_id",
        "habitation_name",
        "habitation_type",
        "population",
        "district",
        "state",
        "geometry"
    ]
]


# -------------------------------------------------
# Save cleaned dataset
# -------------------------------------------------

output_file = os.path.join(
    output_folder,
    "pune_habitations.gpkg"
)

pune_habitations.to_file(
    output_file,
    layer="habitations",
    driver="GPKG"
)


# -------------------------------------------------
# Summary
# -------------------------------------------------

print("\n--------------------------------")
print("Habitation dataset created")
print("--------------------------------")

print("Total habitations:", len(pune_habitations))

print("\nHabitation types:")
print(
    pune_habitations["habitation_type"]
    .value_counts()
    .to_string()
)

print("\nOutput:")
print(output_file)