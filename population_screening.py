import geopandas as gpd
import os

# -------------------------------------------------
# Settings
# -------------------------------------------------

INPUT_FILE = "data/processed/pune_habitations.gpkg"
OUTPUT_FOLDER = "data/processed"

POPULATION_THRESHOLD = 5000


# -------------------------------------------------
# Load habitation dataset
# -------------------------------------------------

habitations = gpd.read_file(
    INPUT_FILE,
    layer="habitations"
)

print("Total habitations:", len(habitations))


# -------------------------------------------------
# Population screening
# -------------------------------------------------

habitations["population_priority"] = (
    habitations["population"] >= POPULATION_THRESHOLD
)


# -------------------------------------------------
# Count results
# -------------------------------------------------

priority = habitations[
    habitations["population_priority"] == True
]

non_priority = habitations[
    habitations["population_priority"] == False
]


print("\n--------------------------------")
print("POPULATION SCREENING")
print("--------------------------------")

print("Population threshold:", POPULATION_THRESHOLD)

print("Priority habitations:", len(priority))

print("Other habitations:", len(non_priority))


# -------------------------------------------------
# Display priority habitations
# -------------------------------------------------

print("\nPriority habitations:")

print(
    priority[
        [
            "habitation_name",
            "habitation_type",
            "population"
        ]
    ]
    .sort_values("population", ascending=False)
    .to_string(index=False)
)


# -------------------------------------------------
# Save result
# -------------------------------------------------

output_file = os.path.join(
    OUTPUT_FOLDER,
    "pune_population_screened.gpkg"
)

habitations.to_file(
    output_file,
    layer="population_screened",
    driver="GPKG"
)


print("\nSaved to:")
print(output_file)