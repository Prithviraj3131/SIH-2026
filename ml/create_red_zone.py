import rasterio
import numpy as np


# -------------------------------------------------
# Paths
# -------------------------------------------------

INPUT_PATH = "data/processed/pune_landslide_susceptibility.tif"

OUTPUT_PATH = "data/processed/pune_landslide_red_zone.tif"


# -------------------------------------------------
# Red-zone threshold
# -------------------------------------------------

RED_THRESHOLD = 0.70


# -------------------------------------------------
# Read susceptibility raster
# -------------------------------------------------

with rasterio.open(INPUT_PATH) as src:

    susceptibility = src.read(1)

    profile = src.profile.copy()


# -------------------------------------------------
# Create red-zone raster
# -------------------------------------------------

red_zone = np.full(
    susceptibility.shape,
    255,
    dtype=np.uint8
)


# Valid pixels
valid = susceptibility != -9999


# Red zone = 1
red_zone[
    valid &
    (susceptibility >= RED_THRESHOLD)
] = 1


# Non-red = 0
red_zone[
    valid &
    (susceptibility < RED_THRESHOLD)
] = 0


# -------------------------------------------------
# Save
# -------------------------------------------------

profile.update(
    dtype="uint8",
    count=1,
    nodata=255
)


with rasterio.open(
    OUTPUT_PATH,
    "w",
    **profile
) as dst:

    dst.write(red_zone, 1)


# -------------------------------------------------
# Statistics
# -------------------------------------------------

valid_red = red_zone[red_zone != 255]

red_pixels = np.sum(valid_red == 1)
non_red_pixels = np.sum(valid_red == 0)

total_pixels = len(valid_red)

print("\nRED ZONE CREATED")
print("----------------")

print("Threshold:", RED_THRESHOLD)

print("Total valid pixels:", total_pixels)

print("Red-zone pixels:", red_pixels)

print("Non-red pixels:", non_red_pixels)

print(
    "Red-zone percentage:",
    round((red_pixels / total_pixels) * 100, 2),
    "%"
)

print("\nSaved to:")
print(OUTPUT_PATH)