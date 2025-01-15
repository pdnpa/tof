# National Parks Analysis in England

## Overview
This repository provides tools and workflows for spatial analysis of the 10 National Parks in England. It focuses on processing, analyzing, and visualizing data related to priority habitats and constraints within these parks. The outputs can be used to support land management, conservation planning, and policy-making.

---

## Objectives
- Cut spatial data to National Park boundaries.
- Create constraints matrices for each National Park.
- Visualize and analyze the relationships between priority habitats, constraints, and remaining areas within National Park boundaries.
- Extend the analysis to all 10 National Parks in England.

---

## Repository Structure
```plaintext
national-parks-analysis/
│
├── data/                  # Raw and processed data
│   ├── boundaries/        # National Park boundaries
│   ├── constraints/       # Constraints data
│   ├── outputs/           # Final shapefiles and analysis results
│
├── scripts/               # Processing and analysis scripts
│   ├── cut_to_boundaries.py
│   ├── create_constraints_matrix.py
│   ├── calculate_statistics.py
│
├── notebooks/             # For exploratory and visualization work
│   ├── visualisation.ipynb
│
├── requirements.txt       # Dependencies
├── README.md              # Documentation
└── LICENSE                # Licensing information (if applicable)
```

---

## Setup and Installation

### Prerequisites
- Python 3.8+
- GeoPandas
- Matplotlib
- PyProj
- Shapely
- Other dependencies (see `requirements.txt`)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/national-parks-analysis.git
   cd national-parks-analysis
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Data Preparation
- Ensure National Park boundaries, constraints, and other datasets are placed in the `data/` directory under the appropriate subfolders.

### 2. Run Scripts

#### Cut Data to National Park Boundaries
Use the `cut_to_boundaries.py` script to clip spatial data to National Park boundaries.
```bash
python scripts/cut_to_boundaries.py --input ./data/constraints --output ./data/outputs --boundary ./data/boundaries
```

#### Create Constraints Matrix
Generate constraints matrices for each park using `create_constraints_matrix.py`:
```bash
python scripts/create_constraints_matrix.py --constraints ./data/outputs --output ./data/outputs/constraints_matrix
```

#### Calculate Statistics
Run `calculate_statistics.py` to calculate areas and overlaps:
```bash
python scripts/calculate_statistics.py --input ./data/outputs/constraints_matrix --output ./data/outputs/statistics.csv
```

### 3. Visualization
Use the notebook `notebooks/visualization.ipynb` to explore and visualize the outputs interactively.

---

## Data Sources
- **National Park Boundaries**: Natural England [National Parks (England)](https://naturalengland-defra.opendata.arcgis.com/datasets/Defra::national-parks-england/about)
- **Priority Habitats**: Natural England [Priority Habitats Inventory (England)](https://naturalengland-defra.opendata.arcgis.com/datasets/39403df11c8044d998772db5b54ad86c_0/explore)
- **Constraints Data**: Derived from multiple sources (e.g., flood zones, land ownership).

---

## Outputs
- **Shapefiles**:
  - Clipped spatial data per National Park.
  - Constraints matrices.
  - Remaining areas.
- **Visualizations**:
  - Maps of priority habitats, constraints, and remaining areas.
- **Statistics**:
  - Area and percentage of priority habitats, constraints, and remaining areas.

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with improvements, bug fixes, or new features.

---


## Contact
For any questions or feedback, open an issue in the repository.

