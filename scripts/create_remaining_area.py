import os
import geopandas as gpd
import pandas as pd

# File paths dictionary
filepaths = {
    "boundary": "../data/boundaries/National_Parks_England/National_Parks_(England)___Natural_England.shp",
    "priority_habitats": "../data/outputs/clipped/priority_habitats_clipped.shp",
    "constraints_matrix": "../data/outputs/constraints_matrix/constraints_matrix_no_habitats.shp",
    "combined_constraints": "../data/outputs/combined_constraints.shp",
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
if not os.path.exists(filepaths["combined_constraints"]):
    print("Combining priority habitats and constraints...")
    combined_constraints = pd.concat([priority_habitats, constraints_matrix], ignore_index=True)
    combined_constraints = gpd.GeoDataFrame(combined_constraints, crs=priority_habitats.crs)

    # Filter for polygons and multipolygons only
    print(f"Filtering {len(combined_constraints)} geometries to include only polygons and multipolygons...")
    combined_constraints = combined_constraints[
        combined_constraints.geometry.type.isin(["Polygon", "MultiPolygon"])
    ]

    # Fix invalid geometries
    print("Fixing invalid geometries...")
    combined_constraints["geometry"] = combined_constraints.geometry.buffer(0)

    # Dissolve to merge overlapping geometries
    print("Dissolving geometries to remove overlaps...")
    combined_constraints = combined_constraints.dissolve()

    # Save the combined constraints
    combined_constraints.to_file(filepaths["combined_constraints"])
    print(f"Combined constraints saved to: {filepaths['combined_constraints']}")
else:
    print("Loading pre-saved combined constraints...")
    combined_constraints = gpd.read_file(filepaths["combined_constraints"])

# Fix invalid geometries in the boundary
print("Fixing invalid geometries in boundary...")
boundary_gdf["geometry"] = boundary_gdf.geometry.buffer(0)

# Clip combined constraints to the boundary
print("Clipping combined constraints to the boundary...")
combined_constraints = gpd.clip(combined_constraints, boundary_gdf)

# Only polygons/multipolygons in combined constraints after clipping
print("Filtering combined constraints after clipping...")
combined_constraints = combined_constraints[
    combined_constraints.geometry.type.isin(["Polygon", "MultiPolygon"])
]

# Subtract combined constraints from the boundary
print("Calculating remaining area...")
remaining_area = gpd.overlay(boundary_gdf, combined_constraints, how="difference")

# Save the remaining area to a shapefile
print("Saving remaining area shapefile...")
remaining_area.to_file(filepaths["remaining_area"])
print(f"Remaining area shapefile saved to: {filepaths['remaining_area']}")

# Calculate and print the area of the remaining region
print("Calculating area statistics...")
remaining_area["area_ha"] = remaining_area.geometry.area / 10000  # Convert to hectares
total_area_ha = remaining_area["area_ha"].sum()
print(f"Total remaining area: {total_area_ha:.2f} hectares")

# Process complete
print("Processing complete.")
