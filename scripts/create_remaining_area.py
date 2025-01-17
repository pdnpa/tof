import os
import geopandas as gpd
import pandas as pd

# File paths dictionary
filepaths = {
    "boundary": "../data/boundaries/National_Parks_England/National_Parks_(England)___Natural_England.shp",
    "priority_habitats": "../data/outputs/clipped/priority_habitats_clipped.shp",
    "constraints_matrix": "../data/outputs/constraints_matrix/constraints_matrix_no_habitats.shp",
    "phi_constraints": "../data/outputs/phi_constraints.shp",
    "remaining_area": "../data/outputs/remaining_area.shp",
}

# Output folder
os.makedirs(os.path.dirname(filepaths["remaining_area"]), exist_ok=True)

# Load the National Parks boundary
print("Loading National Parks boundary...")
boundary_gdf = gpd.read_file(filepaths["boundary"])

# Load the priority habitats and constraints matrix
print("Loading priority habitats and constraints matrix...")
priority_habitats = gpd.read_file(filepaths["priority_habitats"])
constraints_matrix = gpd.read_file(filepaths["constraints_matrix"])

# Combine priority habitats and constraints into one dataset
print("Combining priority habitats and constraints...")
phi_constraints = pd.concat([priority_habitats, constraints_matrix], ignore_index=True)
phi_constraints = gpd.GeoDataFrame(phi_constraints, crs=priority_habitats.crs)

# Dissolve to combine overlapping geometries into a single layer
print("Dissolving combined constraints...")
phi_constraints = phi_constraints.dissolve()

# Save the merged layer as phi_constraints.shp
phi_constraints.to_file(filepaths["phi_constraints"])
print(f"phi_constraints shapefile saved to: {filepaths['phi_constraints']}")

# Fix invalid geometries in the boundary
print("Fixing invalid geometries in boundary...")
boundary_gdf["geometry"] = boundary_gdf.geometry.buffer(0)

# Calculate the remaining area (Boundary - phi_constraints)
print("Calculating remaining area...")
remaining_area = gpd.overlay(boundary_gdf, phi_constraints, how="difference")

# Save the remaining area shapefile
print("Saving remaining area shapefile...")
remaining_area.to_file(filepaths["remaining_area"])
print(f"Remaining area shapefile saved to: {filepaths['remaining_area']}")

# Calculate and print the area of the remaining region
print("Calculating area statistics...")
remaining_area["area_ha"] = remaining_area.geometry.area / 10000  # Convert to hectares
total_area_ha = remaining_area["area_ha"].sum()
print(f"Total remaining area: {total_area_ha:.2f} hectares")

# Processing complete
print("Processing complete.")
