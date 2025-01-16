import os
import geopandas as gpd
import pandas as pd

# Paths
landcover_base_path = "../data/landcover/mlcnp_data/"
remaining_area_path = "../data/outputs/remaining_area.shp"
output_clipped_path = "../data/outputs/landcover_clipped/"
output_csv_path = "../data/outputs/landcover_statistics.csv"

# List of National Parks and folders
parks = {
    "broads": "Broads",
    "dales": "Yorkshire Dales",
    "dartmoor": "Dartmoor",
    "exmoor": "Exmoor",
    "lakes": "Lake District",
    "northum": "Northumberland",
    "nym": "North York Moors",
    "peak": "Peak District",
    "south_downs": "South Downs",
    "new_forest": "New Forest"
}

# Output folder
os.makedirs(output_clipped_path, exist_ok=True)

# Load remaining area shapefile
print("Loading remaining area shapefile...")
remaining_area_gdf = gpd.read_file(remaining_area_path)

# s a DataFrame to store results
result_df = pd.DataFrame(index=parks.values(), columns=[f"ATTR4_{i}" for i in range(1, 51)])
result_df.index.name = "National Park"

# Process each park
for folder, park_name in parks.items():
    if park_name in ["South Downs", "New Forest"]:
        print(f"No data for {park_name}. Marking as 'n/a'...")
        result_df.loc[park_name] = "n/a"
        continue

    landcover_path = os.path.join(landcover_base_path, folder, "mos80a.shp")
    if not os.path.exists(landcover_path):
        print(f"Landcover file not found for {park_name}. Skipping...")
        result_df.loc[park_name] = "n/a"
        continue

    print(f"Processing {park_name}...")
    # Load the landcover shapefile
    landcover_gdf = gpd.read_file(landcover_path)

    # Clip to the remaining area
    clipped_landcover = gpd.clip(landcover_gdf, remaining_area_gdf)

    # Save the clipped shapefile
    clipped_output_path = os.path.join(output_clipped_path, f"{folder}_clipped.shp")
    clipped_landcover.to_file(clipped_output_path)
    print(f"Clipped landcover saved to: {clipped_output_path}")

    # Calculate area for each ATTR4 value
    clipped_landcover["area_ha"] = clipped_landcover.geometry.area / 10000  # Convert to hectares
    attr4_stats = clipped_landcover.groupby("ATTR4")["area_ha"].sum()

    # Add results to the DataFrame
    for attr4, area in attr4_stats.items():
        result_df.loc[park_name, f"ATTR4_{int(attr4)}"] = area

# Save results to CSV
print("Saving results to CSV...")
result_df.to_csv(output_csv_path)
print(f"Results saved to: {output_csv_path}")

print("Processing complete.")
