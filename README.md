# Building-to-Building Accessibility Network Analysis

A Python project that extracts building connectivity networks from CityGML data to demonstrate transportation/mobility network analysis concepts. This project showcases computational approaches in infrastructure planning and network optimization.

**Research Alignment (WPI - Dr. Lindsay Graff):**
- Network optimization in multi-modal transportation systems
- Computational approaches to infrastructure planning
- Graph-based analysis of connectivity and accessibility
- Integration of human behavioral insights into transportation system design

---

## 🎯 Project Overview

This project processes CityGML building data to:
1. Extract building footprints and metadata
2. Construct connectivity networks between buildings
3. Analyze network properties (centrality, shortest paths)
4. Calculate accessibility metrics
5. Visualize results

The pipeline demonstrates how building-level spatial data can be analyzed using network science methods, directly applicable to transportation network optimization and infrastructure planning.

---

## 📋 Project Structure

```
mobility-network-analysis/
├── README.md                          # This file
├── PROJECT_PLAN.md                    # Detailed project plan
├── PIPELINE_COMPLETE.md               # Pipeline completion summary
├── TEST_RESULTS.md                    # Test results documentation
├── requirements.txt                   # Python dependencies
├── data/
│   ├── input/                         # CityGML input files
│   ├── processed/                     # Intermediate data (CSV, pickle)
│   └── output/                        # Final outputs (PNG visualizations)
├── scripts/
│   ├── 1_extract_buildings.py         # Step 1: Extract buildings from CityGML
│   ├── 2_build_network.py             # Step 2: Build network graph
│   ├── 3_analyze_network.py           # Step 3: Network analysis
│   ├── 4_calculate_accessibility.py  # Step 4: Accessibility scoring
│   ├── 5_visualize_network.py        # Step 5: Visualization
│   ├── run_pipeline.py                # Complete pipeline runner
│   └── combine_footprints.py          # Utility: Combine footprint files
├── utils/
│   ├── gml_parser.py                  # CityGML parsing utilities
│   ├── network_utils.py               # Network analysis utilities
│   └── visualization_utils.py         # Visualization helpers
└── tests/
    └── test_pipeline.py               # Test script
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Complete Pipeline

```bash
python scripts/run_pipeline.py --input "gml_files/*.gml" --output data/output/ --threshold 500
```

### 3. Run Individual Steps

```bash
# Step 1: Extract buildings
python scripts/1_extract_buildings.py --input data/input/sample.gml --output data/processed/buildings.csv

# Step 2: Build network
python scripts/2_build_network.py --input data/processed/buildings.csv --output data/processed/graph.pkl --threshold 500

# Step 3: Analyze network
python scripts/3_analyze_network.py --input data/processed/graph.pkl --output data/processed/metrics.csv

# Step 4: Calculate accessibility
python scripts/4_calculate_accessibility.py --input data/processed/buildings.csv --graph data/processed/graph.pkl --output data/processed/accessibility.csv

# Step 5: Visualize
python scripts/5_visualize_network.py --buildings data/processed/buildings.csv --graph data/processed/graph.pkl --metrics data/processed/metrics.csv --accessibility data/processed/accessibility.csv --output data/output/
```

---

## 📊 Pipeline Steps

### Step 1: Building Extraction
- Parses CityGML files (supports MultiSurface, EPSG:5253, Turkish GML format)
- Extracts building footprints (ground surface polygons)
- Extracts metadata (ID, centroid, area, height, type)
- Transforms coordinates (EPSG:5253 → WGS84)
- Outputs: `buildings_geodata.csv`, `footprints.pkl`

### Step 2: Network Construction
- Calculates building-to-building distances (Haversine)
- Creates network graph (NetworkX)
- Supports distance-based and Delaunay triangulation methods
- Calculates network statistics
- Outputs: `building_network_graph.pkl`, `network_stats.json`, `edges.csv`

### Step 3: Network Analysis
- Calculates shortest paths (Dijkstra algorithm)
- Computes centrality metrics:
  - Degree Centrality
  - Betweenness Centrality
  - Closeness Centrality
  - PageRank
- Outputs: `network_metrics.csv`, `network_paths.json`

### Step 4: Accessibility Scoring
- Distance-based accessibility (buildings within threshold)
- Network-based accessibility (reachable via network)
- Average path distances
- Weighted accessibility (area-based)
- Outputs: `accessibility_metrics.csv`

### Step 5: Visualization
- Network graph visualization (nodes, edges, centrality coloring)
- Accessibility heatmap
- Optimal paths visualization
- Degree distribution
- Centrality comparison charts
- Outputs: Multiple PNG files in `data/output/`

---

## 🛠️ Technical Details

### Key Features

1. **Multi-format Support:**
   - CityGML 2.0 with MultiSurface
   - EPSG:5253 (Turkish projected CRS) → WGS84 transformation
   - Turkish character handling and translation

2. **Network Analysis:**
   - Graph-based connectivity analysis
   - Multiple centrality metrics
   - Shortest path algorithms
   - Network statistics

3. **Accessibility Metrics:**
   - Distance-based (Euclidean/Haversine)
   - Network-based (graph traversal)
   - Weighted by building area

4. **Visualization:**
   - Static network graphs (matplotlib)
   - Heatmaps and distribution plots
   - Multiple visualization types

### Dependencies

- `lxml`: CityGML parsing
- `shapely`: Geometric operations
- `geopandas`: Geospatial data handling
- `networkx`: Network analysis
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `matplotlib`: Visualization
- `pyproj`: Coordinate transformations
- `geopy`: Distance calculations
- `scipy`: Spatial analysis

### Data Formats

- **Input:** CityGML (.gml) files
- **Output:** 
  - CSV files (building data, metrics)
  - JSON files (paths, statistics)
  - PNG files (visualizations)
  - Pickle files (graphs, footprints)

---

## 📈 Example Results

### Test Dataset
- **Input:** 2 CityGML files (Turkish cadastral data)
- **Buildings Extracted:** 2 buildings
- **Network:** 2 nodes, 1 edge (347.27m distance)

### Network Metrics
- **Degree Centrality:** 1.0 (both buildings)
- **Betweenness Centrality:** 0.0 (no intermediate nodes)
- **Closeness Centrality:** 0.0029
- **PageRank:** 0.5 (equal importance)

### Accessibility Metrics
- **Distance Accessibility (500m):** 1.0 (each building has 1 neighbor)
- **Network Accessibility:** 1.0 (each building can reach 1 other)
- **Average Path Distance:** 347.27m

---

## 🎓 Research Applications

This project demonstrates:

1. **Network Optimization Concepts:**
   - Shortest path algorithms
   - Centrality metrics for identifying critical nodes
   - Graph-based connectivity analysis

2. **Infrastructure Planning:**
   - Building connectivity analysis
   - Accessibility assessment
   - Spatial network construction

3. **Computational Methods:**
   - Scalable data processing pipeline
   - Automated analysis workflows
   - Multi-format data integration

4. **Transportation Network Concepts:**
   - Building connectivity → transportation connectivity analogy
   - Graph-based thinking for network design
   - Accessibility metrics for service planning

---

## 📝 Documentation

- **PROJECT_PLAN.md:** Detailed project plan and architecture
- **PIPELINE_COMPLETE.md:** Pipeline completion summary
- **TEST_RESULTS.md:** Test results and observations
- **ADIM_1_2_OZET.md:** Detailed explanation of Steps 1-2 (Turkish)

---

## 🔧 Configuration

### Network Construction Parameters

- **Distance Threshold:** Maximum distance (meters) for edge creation
  - Default: 200m (walkable distance)
  - Recommended: 500m (extended walking distance)
  
- **Method:** Network construction method
  - `distance`: Distance-based threshold
  - `delaunay`: Delaunay triangulation (nearest neighbors)

### Accessibility Parameters

- **Distance Threshold:** Maximum distance for accessibility calculation
  - Default: 500m
  - Adjustable based on use case

---

## 🐛 Known Issues / Future Improvements

1. **Area Calculation:** Currently uses source CRS; should use projected CRS for accuracy
2. **Large Datasets:** O(n²) complexity for distance calculation; optimization needed
3. **Road Network:** Road data integration not implemented (future work)
4. **3D Analysis:** Height information not fully utilized
5. **Interactive Visualization:** Currently static; Plotly integration planned

---

## 👤 Author

**Süleyman Sarılar**
- Architecture graduate (Pamukkale University)
- Research focus: Construction AI, BIM Analytics, Digital Twin, VR/UX
- GitHub: https://github.com/suleymansarilar

---

## 📄 License

MIT License

---

## 🙏 Acknowledgments

This project was developed as part of PhD application preparation for:
- **WPI - Dr. Lindsay Graff** (Transportation Systems & Network Optimization)
- Research alignment: Multi-modal transportation systems, infrastructure planning, network optimization

---

## 📚 References

- CityGML Specification: https://www.ogc.org/standards/citygml
- NetworkX Documentation: https://networkx.org/
- Shapely Documentation: https://shapely.readthedocs.io/
- Haversine Formula: https://en.wikipedia.org/wiki/Haversine_formula

---

## 🔗 Related Projects

- [BIM Analytics & Safety Rules](https://github.com/suleymansarilar/bim-analytics-safety-rules)
- [BIM VR Walkthrough](https://github.com/suleymansarilar/bim-vr-walkthrough)
