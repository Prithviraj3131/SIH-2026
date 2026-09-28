import geopandas as gpd

# -------------------------------------------------
# File paths
# -------------------------------------------------

state_file = "data/boundaries/india_states.geojson"
osm_file = "data/osm/western-zone.gpkg"


# -------------------------------------------------
# Load state boundaries
# -------------------------------------------------

states = gpd.read_file(state_file)

print("States loaded:", len(states))
print("State CRS:", states.crs)


# -------------------------------------------------
# Load district boundaries
# -------------------------------------------------

districts = gpd.read_file(
    osm_file,
    layer="gis_osm_adminareas_a_free"
)

# Keep only district boundaries
districts = districts[
    districts["fclass"] == "admin_level5"
].copy()

print("Districts loaded:", len(districts))
print("District CRS:", districts.crs)


# -------------------------------------------------
# Convert district CRS to state CRS
# -------------------------------------------------

districts = districts.to_crs(states.crs)


# -------------------------------------------------
# Create a point guaranteed to be inside
# each district
# -------------------------------------------------

district_points = districts.copy()

district_points["geometry"] = (
    district_points.geometry.representative_point()
)


# -------------------------------------------------
# Spatial join
# -------------------------------------------------

district_with_state = gpd.sjoin(
    district_points,
    states[["state_name", "stcode", "geometry"]],
    how="left",
    predicate="within"
)


# -------------------------------------------------
# Display results
# -------------------------------------------------

print("\nDistrict → State mapping:\n")

print(
    district_with_state[
        ["name", "state_name", "stcode"]
    ].to_string(index=False)
)