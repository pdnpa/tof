# National Parks Analysis in England

## Overview
This repository provides tools and workflows for spatial analysis of the 10 National Parks in England. It focuses on processing, analyzing, and visualizing data related to priority habitats, constraints, and remaining areas within these parks. The outputs support land management, conservation planning, and policy-making.

---

## Objectives
- Clip spatial data to National Park boundaries.
- Generate constraints matrices for each National Park.
- Visualize and analyze the relationships between priority habitats, constraints, and remaining areas within National Park boundaries.
- Extend the analysis to all 10 National Parks in England with reproducible workflows.

---

## Repository Structure
```plaintext
national-parks-analysis/
│
├── data/                  # Raw and processed data
│   ├── boundaries/        # National Park boundaries
│   ├── constraints/       # Constraints data
│   ├── outputs/           # Final shapefiles, statistics, and visualizations
│       ├── clipped/       # Clipped data by National Park
│       ├── constraints_matrix/ # Merged constraints and final outputs
│       ├── visualizations/ # Saved maps and plots
│
├── scripts/               # Processing and analysis scripts
│   ├── cut_to_boundaries.py
│   ├── create_constraints_matrix.py
│   ├── calculate_statistics.py
│
├── notebooks/             # Interactive visualization and exploratory work
│   ├── visualization.ipynb
│
├── requirements.txt       # Dependencies (optional, pip-based installs)
├── environment.yml        # Conda environment file
├── README.md              # Documentation

```

---

## Setup and Installation

### Prerequisites
- Python 3.8+
- Required Python libraries:
  - GeoPandas
  - Matplotlib
  - PyProj
  - Shapely
  - Pandas
  - tqdm

### Installation Steps

#### Using Conda (Recommended)
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/national-parks-analysis.git
   cd national-parks-analysis
   ```
2. Create the environment from the `environment.yml` file:
   ```bash
   conda env create -f environment.yml
   ```
3. Activate the environment:
   ```bash
   conda activate tof
   ```

#### Using `requirements.txt` (Optional)
If you prefer `pip`, use:
```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Data Preparation
- Ensure National Park boundaries, constraints, and other datasets are placed in the `data/` directory under the appropriate subfolders.
- Supported file formats: `.shp`, `.gpkg`, or other GeoDataFrame-compatible formats.

### 2. Run Scripts

#### Clip Data to National Park Boundaries
Use the `cut_to_boundaries.py` script to clip spatial data to National Park boundaries:
```bash
python scripts/cut_to_boundaries.py
```
This script:
- Clips datasets in the `constraints/` folder to the National Parks boundary.
- Filters geometry types to polygons.

#### Generate Constraints Matrix
Generate constraints matrices with the `create_constraints_matrix.py` script:
```bash
python scripts/create_constraints_matrix.py
```
This script:
- Merges clipped constraints into a single dataset.
- Excludes priority habitats to calculate available areas.

#### Calculate and Save Statistics
Use `calculate_statistics.py` to compute areas and percentages:
```bash
python scripts/calculate_statistics.py
```
This script:
- Saves statistics as CSV files for further analysis.

### 3. Visualization
Use the `notebooks/visualization.ipynb` notebook to generate and customize visual outputs. Key visualizations include:
- 10 National Parks with priority habitats, constraints, and remaining areas.
- Statistics displayed below each National Park map.

---

## Data Sources
- **National Park Boundaries**: [Natural England - National Parks (England)](https://naturalengland-defra.opendata.arcgis.com/datasets/Defra::national-parks-england/about)
- **Priority Habitats**: [Priority Habitats Inventory (England)](https://naturalengland-defra.opendata.arcgis.com/datasets/39403df11c8044d998772db5b54ad86c_0/explore)
- **Constraints Data**: Sourced from multiple agencies (e.g., OS Data, CEH Lakes, SSSI datasets).

---

## Outputs
1. **Clipped Data**:
   - Individual layers clipped to each National Park boundary.
2. **Constraints Matrix**:
   - Combined constraints dataset, with and without priority habitats.
3. **Statistics**:
   - CSV files with areas (hectares) and percentages for:
     - National Parks.
     - Priority habitats.
     - Constraints matrix.
4. **Visualizations**:
   - Subplots showing all 10 National Parks.
   - Maps with key statistics.

---

## Example Outputs
### Area Statistics (CSV)
Saved to `../output/national_parks_area_stats.csv`:
```csv
park_name,total_area_ha,priority_area_ha,constraints_area_ha,priority_pct,constraints_pct
Peak District,144768.25,52534.40,41237.70,36.3,28.5
Lake District,226813.50,81241.60,50122.30,35.8,22.1
...
```

### Maps
Saved to `../output/national_parks_with_stats.png`.

---

## Contributing
Contributions are welcome! Feel free to:
- Open issues for bugs or feature requests.
- Submit pull requests with improvements or new functionality.

---

## Contact
For any questions or feedback, please open an issue in this repository.

---

