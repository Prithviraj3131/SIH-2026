import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np


# -------------------------------------------------
# Paths
# -------------------------------------------------

HABITATIONS_PATH = "data/processed/pune_habitations.gpkg"
RED_ZONE_PATH = "data/processed/pune_landslide_red_zone.tif"

OUTPUT_PATH = "data/processed/pune_red_zone_habitations.gpkg"


# -------------------------------------------------
# Load habitations
# -------------------------------------------------

print("Loading habitations...")

habitations = gpd.read_file(HABITATIONS_PATH)

print(f"Total habitations: {len(habitations)}")


# -------------------------------------------------
# Open red-zone raster
# -------------------------------------------------

print("Opening red-zone raster...")

with rasterio.open(RED_ZONE_PATH) as src:

    # Convert habitation coordinates
    # to the raster CRS
    habitations = habitations.to_crs(src.crs)

    red_zone_values = []

    for point in habitations.geometry:

        try:
            row, col = src.index(point.x, point.y)

            # Check if point is inside raster
            if (
                row < 0
                or row >= src.height
                or col < 0
                or col >= src.width
            ):
                red_zone_values.append(255)
                continue

            value = src.read(1)[row, col]

            red_zone_values.append(value)

        except Exception:
            red_zone_values.append(255)


# -------------------------------------------------
# Add red-zone classification
# -------------------------------------------------

habitations["red_zone"] = np.array(red_zone_values)

habitations["red_zone"] = habitations["red_zone"].map({
    0: "No",
    1: "Yes",
    255: "NoData"
})


# -------------------------------------------------
# Keep only red-zone habitations
# -------------------------------------------------

red_habitations = habitations[
    habitations["red_zone"] == "Yes"
].copy()


# -------------------------------------------------
# Save result
# -------------------------------------------------

red_habitations.to_file(
    OUTPUT_PATH,
    layer="red_zone_habitations",
    driver="GPKG"
)


# -------------------------------------------------
# Summary
# -------------------------------------------------

print()
print("RED-ZONE HABITATIONS")
print("--------------------")
print(f"Total habitations: {len(habitations)}")
print(f"Red-zone habitations: {len(red_habitations)}")

print()

if len(red_habitations) > 0:

    print("Habitation types:")

    print(
        red_habitations["habitation_type"]
        .value_counts()
    )

    print()

    print("Population information:")

    print(
        red_habitations["population"].describe()
    )

else:

    print("No habitations found inside the red zone.")


print()
print("Saved to:")
print(OUTPUT_PATH)