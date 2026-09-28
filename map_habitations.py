import geopandas as gpd

# -------------------------------------------------
# File paths
# -------------------------------------------------

osm_file = "data/osm/western-zone.gpkg"


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
# Select Pune district
# -------------------------------------------------

pune = districts[
    districts["name"].str.lower() == "pune"
].copy()

print("Pune district found:", len(pune))


# -------------------------------------------------
# Load habitation/place points
# -------------------------------------------------

places = gpd.read_file(
    osm_file,
    layer="gis_osm_places_free"
)

print("Total places in Western Zone:", len(places))


# -------------------------------------------------
# Make sure both layers use same CRS
# -------------------------------------------------

places = places.to_crs(pune.crs)


# -------------------------------------------------
# Find places inside Pune
# -------------------------------------------------

pune_places = gpd.sjoin(
    places,
    pune[["name", "geometry"]],
    how="inner",
    predicate="within"
)


# -------------------------------------------------
# Display results
# -------------------------------------------------

print("\nPlaces inside Pune:", len(pune_places))

print("\nFirst 30 places:")

print(
    pune_places[
        ["name_left", "fclass", "population"]
    ].head(30).to_string(index=False)
)
print("\nPlace types inside Pune:")

print(
    pune_places["fclass"]
    .value_counts()
    .to_string()
)