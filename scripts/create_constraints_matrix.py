import os
import geopandas as gpd
import pandas as pd
from tqdm import tqdm  # Import tqdm for progress bar

# File paths dictionary
filepaths = {
    "boundary": "../data/boundaries/National_Parks_England/National_Parks_(England)___Natural_England.shp",
    "priority_habitats": "../data/outputs/clipped/priority_habitats_clipped.shp",
    "constraints_folder": "../data/outputs/clipped/",
    "merged_constraints": "../data/outputs/constraints_matrix/merged_constraints.shp",
    "final_output": "../data/outputs/constraints_matrix/constraints_matrix_no_habitats.shp",
}

# Output folder 
os.makedirs(os.path.dirname(filepaths["merged_constraints"]), exist_ok=True)

# Load the National Parks boundary
boundary_gdf = gpd.read_file(filepaths["boundary"])

# Fix and validate boundary geometries (some are invalid)
boundary_gdf["geometry"] = boundary_gdf.geometry.buffer(0)

# Initialize 
constraints_list = []

# Loop through each file in the constraints folder with a progress bar
print("Processing constraint files...")
for filename in tqdm(os.listdir(filepaths["constraints_folder"])):
    if filename.endswith(".shp"):
        input_path = os.path.join(filepaths["constraints_folder"], filename)

        print(f"Processing file: {filename}")

        # Load 
        constraint_gdf = gpd.read_file(input_path)

        # Fix 
        constraint_gdf["geometry"] = constraint_gdf.geometry.buffer(0)

        # Clip 
        try:
            clipped_gdf = gpd.clip(constraint_gdf, boundary_gdf)
            constraints_list.append(clipped_gdf)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue

# Merge all constraints into a single GeoDataFrame
if constraints_list:
    merged_constraints = gpd.GeoDataFrame(
        pd.concat(constraints_list, ignore_index=True), crs=constraints_list[0].crs
    )

    # Ensure the merged GeoDataFrame contains only polygon geometries
    merged_constraints = merged_constraints[merged_constraints.geometry.type == "Polygon"]

    # Fix 
    merged_constraints["geometry"] = merged_constraints.geometry.buffer(0)

    # Resolve topology issues by dissolving overlapping geometries
    merged_constraints = merged_constraints.dissolve()

    # Save 
    merged_constraints.to_file(filepaths["merged_constraints"])
    print(f"Merged constraints saved to: {filepaths['merged_constraints']}")
else:
    print("No valid constraints found to merge.")

# Load priority habitats
priority_habitats = gpd.read_file(filepaths["priority_habitats"])

# Fix 
priority_habitats["geometry"] = priority_habitats.geometry.buffer(0)

# Resolve topology issues in priority habitats
priority_habitats = priority_habitats.dissolve()

# Subtract priority habitats from the constraints
if not merged_constraints.empty:
    print("Subtracting priority habitats from merged constraints...")
    constraints_minus_habitats = gpd.overlay(merged_constraints, priority_habitats, how="difference")

    # Save 
    constraints_minus_habitats.to_file(filepaths["final_output"])
    print(f"Final constraints matrix (excluding habitats) saved to: {filepaths['final_output']}")
else:
    print("Merged constraints are empty; skipping subtraction.")

print("Processing complete.")
