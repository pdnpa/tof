import os
import geopandas as gpd

"""
This script clips data to the combined boundaries of all National Parks in England. 
It ensures only polygon or multipolygon geometries are processed.
"""

# File paths dictionary
filepaths = {
    "boundary": "../data/boundaries/National_Parks_England/National_Parks_(England)___Natural_England.shp",  # National Parks boundary
    "constraints": {
        "registered_parks": "../data/constraints/National_Heritage_List_for_England.gpkg",
        #"open_rivers": "../data/constraints/oprvrs_gb.gpkg", # not going to use this now unless required
        "built_up_land": "../data/constraints/os_open_built_up_areas.gpkg",
        "SSSI": "../data/constraints/SSSI_England.gpkg",
        "UK_lakes_CEH": "../data/constraints/uklakes_v3_6_poly.gpkg",
    },
    "priority_habitats": "../data/priority-habitats/Priority_Habitats_Inventory_England.gpkg",
    "output": "../data/outputs/clipped/",
}

# Output folder
os.makedirs(filepaths["output"], exist_ok=True)

# Load t
boundary_gdf = gpd.read_file(filepaths["boundary"])

# Ensure valid 
boundary_gdf = boundary_gdf[boundary_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]
boundary_gdf = boundary_gdf.buffer(0)  # Fix invalid geometries

# Loop through the dictionary and clip it to the National Park boundaries
for name, input_path in filepaths["constraints"].items():
    output_path = os.path.join(filepaths["output"], f"{name}_clipped.shp")

    try:
        # Try loading with default encoding
        constraint_gdf = gpd.read_file(input_path)
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError for {input_path}. Retrying with 'latin1' encoding...")
        constraint_gdf = gpd.read_file(input_path, encoding="latin1")

    # Filter for polygons and multipolygons only
    constraint_gdf = constraint_gdf[constraint_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]
    print(f"{name} has {len(constraint_gdf)} polygon features before clipping.")

    # Clip
    clipped_gdf = gpd.clip(constraint_gdf, boundary_gdf)

    # Filter clipped data for polygons and multipolygons
    clipped_gdf = clipped_gdf[clipped_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]
    print(f"{name} has {len(clipped_gdf)} polygon features after clipping.")

    # Save the clipped file
    clipped_gdf.to_file(output_path)
    print(f"Clipped {name} saved to {output_path}")

# Clip the priority habitats to the National Park boundaries
priority_habitats_path = filepaths["priority_habitats"]
priority_habitats_output_path = os.path.join(filepaths["output"], "priority_habitats_clipped.shp")

try:
    priority_habitats_gdf = gpd.read_file(priority_habitats_path)
except UnicodeDecodeError:
    print(f"UnicodeDecodeError for {priority_habitats_path}. Retrying with 'latin1' encoding...")
    priority_habitats_gdf = gpd.read_file(priority_habitats_path, encoding="latin1")

# Filter for polygons and multipolygons only
priority_habitats_gdf = priority_habitats_gdf[priority_habitats_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]
print(f"Priority habitats have {len(priority_habitats_gdf)} polygon features before clipping.")

# Clip
priority_habitats_clipped = gpd.clip(priority_habitats_gdf, boundary_gdf)

# Filter clipped data for polygons and multipolygons (again)
priority_habitats_clipped = priority_habitats_clipped[priority_habitats_clipped.geometry.type.isin(["Polygon", "MultiPolygon"])]
print(f"Priority habitats have {len(priority_habitats_clipped)} polygon features after clipping.")

# Save 
priority_habitats_clipped.to_file(priority_habitats_output_path)
print(f"Clipped priority habitats saved to {priority_habitats_output_path}")
