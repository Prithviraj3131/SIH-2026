import geopandas as gpd

file_path = "data/osm/western-zone.gpkg"

districts = gpd.read_file(
    file_path,
    layer="gis_osm_adminareas_a_free"
)

# Keep only district-level boundaries
districts = districts[
    districts["fclass"] == "admin_level5"
]

print("Number of district boundaries:", len(districts))

print("\nColumns:")
print(districts.columns.tolist())

print("\nCRS:")
print(districts.crs)

print("\nGeometry types:")
print(districts.geometry.geom_type.value_counts())

print("\nDistrict names:")
print(districts["name"].head(30).tolist())