# User Guide - Building-to-Building Accessibility Network Analysis

## 📖 Introduction

This guide will help you use the Building-to-Building Accessibility Network Analysis project. You'll learn how to set up the project, prepare your data, run the analysis pipeline, and interpret the results.

---

## 🚀 Getting Started

### Step 1: Clone the Repository

```bash
git clone https://github.com/suleymansarilar/mobility-network-analysis.git
cd mobility-network-analysis
```

### Step 2: Install Dependencies

Make sure you have Python 3.8+ installed, then install required packages:

```bash
pip install -r requirements.txt
```

**Expected output:** All packages installed successfully.

### Step 3: Prepare Your Data

You need CityGML files containing building data. Place your `.gml` files in the `data/input/` directory:

```bash
# Create input directory if it doesn't exist
mkdir -p data/input

# Copy your GML files
cp /path/to/your/buildings.gml data/input/
```

**Requirements for GML files:**
- Must contain `bldg:Building` elements
- Should have `bldg:lod0FootPrint` or `bldg:GroundSurface` for building footprints
- Supported formats: CityGML 2.0, with or without MultiSurface
- Coordinate systems: WGS84 (EPSG:4326) or projected CRS (will be transformed automatically)

---

## 🎯 Running the Analysis

### Option 1: Complete Pipeline (Recommended)

Run the entire pipeline with one command:

```bash
python scripts/run_pipeline.py --input "data/input/*.gml" --output data/output/ --threshold 500
```

**Parameters:**
- `--input`: Pattern for GML files (e.g., `"data/input/*.gml"` or specific file path)
- `--output`: Output directory for visualizations
- `--threshold`: Distance threshold in meters for network construction (default: 500)

**What it does:**
1. Extracts buildings from all GML files
2. Builds network graph
3. Analyzes network properties
4. Calculates accessibility metrics
5. Creates visualizations

### Option 2: Step-by-Step Execution

Run each step individually for more control:

#### Step 1: Extract Buildings

```bash
python scripts/1_extract_buildings.py --input data/input/your_file.gml --output data/processed/buildings.csv
```

**Output:**
- `buildings.csv`: Building data (ID, centroid, area, height, type)
- `buildings_footprints.pkl`: Building footprint polygons

#### Step 2: Build Network Graph

```bash
python scripts/2_build_network.py --input data/processed/buildings.csv --output data/processed/graph.pkl --threshold 500
```

**Parameters:**
- `--threshold`: Maximum distance (meters) for edge creation
- `--method`: `distance` (default) or `delaunay`
- `--use-edge-distance`: Use edge-to-edge distance instead of centroid

**Output:**
- `graph.pkl`: NetworkX graph
- `graph_stats.json`: Network statistics
- `graph_edges.csv`: Edge list

#### Step 3: Analyze Network

```bash
python scripts/3_analyze_network.py --input data/processed/graph.pkl --output data/processed/metrics.csv
```

**Output:**
- `metrics.csv`: Centrality metrics (degree, betweenness, closeness, PageRank)
- `paths.json`: Shortest paths between buildings

#### Step 4: Calculate Accessibility

```bash
python scripts/4_calculate_accessibility.py --input data/processed/buildings.csv --graph data/processed/graph.pkl --output data/processed/accessibility.csv --threshold 500
```

**Output:**
- `accessibility.csv`: Accessibility metrics (distance-based, network-based, weighted)

#### Step 5: Visualize Results

```bash
python scripts/5_visualize_network.py --buildings data/processed/buildings.csv --graph data/processed/graph.pkl --metrics data/processed/metrics.csv --accessibility data/processed/accessibility.csv --output data/output/
```

**Output:**
- `network_graph.png`: Network visualization
- `accessibility_heatmap.png`: Accessibility heatmap
- `optimal_paths.png`: Shortest paths visualization
- `degree_distribution.png`: Degree distribution
- `centrality_comparison.png`: Centrality metrics comparison

---

## 📊 Understanding the Results

### Output Files Location

- **Processed Data:** `data/processed/`
- **Visualizations:** `data/output/`

### Key Output Files

1. **`all_buildings.csv`**
   - Columns: `building_id`, `centroid_lon`, `centroid_lat`, `area_m2`, `height_m`, `building_type`, `usage`
   - Contains extracted building information

2. **`network_metrics.csv`**
   - Columns: `building_id`, `degree`, `degree_centrality`, `betweenness_centrality`, `closeness_centrality`, `pagerank`
   - Network importance metrics for each building

3. **`accessibility_metrics.csv`**
   - Columns: `building_id`, `distance_500m_count`, `network_reachable_count`, `avg_path_distance_m`, `weighted_accessibility`
   - Accessibility scores for each building

4. **Visualizations (PNG files)**
   - Network graphs, heatmaps, and analysis charts

---

## ⚙️ Configuration Options

### Network Construction Threshold

The distance threshold determines which buildings are connected:

- **200m:** Dense urban areas, close neighbors only
- **500m:** Standard walking distance (recommended)
- **1000m:** Extended walking distance, sparse networks

**Example:**
```bash
python scripts/2_build_network.py --input buildings.csv --output graph.pkl --threshold 1000
```

### Network Construction Method

- **`distance`** (default): Connect buildings within threshold distance
- **`delaunay`**: Use Delaunay triangulation (connects nearest neighbors)

**Example:**
```bash
python scripts/2_build_network.py --input buildings.csv --output graph.pkl --method delaunay
```

### Accessibility Threshold

Distance threshold for accessibility calculations:

```bash
python scripts/4_calculate_accessibility.py --input buildings.csv --graph graph.pkl --output accessibility.csv --threshold 500
```

---

## 🔍 Interpreting Results

### Network Metrics

- **Degree:** Number of connections (higher = more connected)
- **Betweenness Centrality:** How many shortest paths pass through (higher = more critical)
- **Closeness Centrality:** Average distance to all others (higher = more central)
- **PageRank:** Importance score (higher = more important)

### Accessibility Metrics

- **Distance Accessibility:** Number of buildings within threshold distance
- **Network Accessibility:** Number of buildings reachable via network
- **Average Path Distance:** Average shortest path distance to all other buildings
- **Weighted Accessibility:** Accessibility weighted by building area

### Visualizations

- **Network Graph:** Shows building connections, node size = degree, color = centrality
- **Accessibility Heatmap:** Color-coded accessibility scores
- **Optimal Paths:** Highlights shortest paths between buildings

---

## 🐛 Troubleshooting

### Problem: "No buildings found in CityGML file"

**Solution:**
- Check that GML file contains `bldg:Building` elements
- Verify namespace declarations are correct
- Ensure buildings are in `core:cityObjectMember` or directly as `bldg:Building`

### Problem: "Graph has no edges"

**Solution:**
- Buildings are too far apart
- Increase threshold: `--threshold 1000`
- Or use Delaunay method: `--method delaunay`

### Problem: "ModuleNotFoundError"

**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: "Coordinate transformation error"

**Solution:**
- Check CRS in GML file
- Ensure `pyproj` is installed correctly
- The parser automatically transforms EPSG:5253 to WGS84

### Problem: "File not found"

**Solution:**
- Use absolute paths if relative paths don't work
- Check file extensions (`.gml`)
- Ensure files are in correct directory

---

## 📝 Example Workflow

### Complete Example

```bash
# 1. Clone repository
git clone https://github.com/suleymansarilar/mobility-network-analysis.git
cd mobility-network-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Prepare data (copy your GML files)
cp /path/to/buildings.gml data/input/

# 4. Run complete pipeline
python scripts/run_pipeline.py --input "data/input/*.gml" --output data/output/ --threshold 500

# 5. Check results
ls data/output/*.png
ls data/processed/*.csv
```

### Custom Analysis

```bash
# Extract buildings
python scripts/1_extract_buildings.py --input data/input/buildings.gml --output data/processed/buildings.csv

# Build network with custom threshold
python scripts/2_build_network.py --input data/processed/buildings.csv --output data/processed/graph.pkl --threshold 1000 --method delaunay

# Analyze network
python scripts/3_analyze_network.py --input data/processed/graph.pkl --output data/processed/metrics.csv

# Calculate accessibility with custom threshold
python scripts/4_calculate_accessibility.py --input data/processed/buildings.csv --graph data/processed/graph.pkl --output data/processed/accessibility.csv --threshold 1000

# Visualize
python scripts/5_visualize_network.py --buildings data/processed/buildings.csv --graph data/processed/graph.pkl --metrics data/processed/metrics.csv --accessibility data/processed/accessibility.csv --output data/output/
```

---

## 💡 Tips and Best Practices

1. **Start Small:** Test with 2-3 buildings first to understand the workflow
2. **Check Logs:** Read console output for warnings and errors
3. **Verify Outputs:** Always check that output files are created
4. **Try Different Thresholds:** Experiment with different distance thresholds
5. **Inspect Visualizations:** Open PNG files to verify results
6. **Large Datasets:** For many buildings (>100), consider using Delaunay method for faster network construction

---

## 📚 Additional Resources

- **README.md:** Project overview and quick start
- **PROJECT_PLAN.md:** Detailed project architecture
- **TEST_RESULTS.md:** Example test results
- **ANALYSIS_REPORT.md:** Sample analysis report
- **TESTING_GUIDE.md:** Comprehensive testing instructions

---

## ❓ Frequently Asked Questions

### Q: Can I use my own CityGML files?

**A:** Yes! Place your `.gml` files in `data/input/` and run the pipeline. The parser supports various CityGML formats.

### Q: What if my buildings are in a different coordinate system?

**A:** The parser automatically detects and transforms coordinates. EPSG:5253 (Turkish CRS) is supported, and other projected CRS will be transformed to WGS84.

### Q: How do I choose the right threshold?

**A:** 
- **200m:** Dense urban, close neighbors
- **500m:** Standard walking distance (recommended)
- **1000m:** Extended distance, sparse networks

Start with 500m and adjust based on your data.

### Q: Can I analyze more than one GML file?

**A:** Yes! Use wildcards: `--input "data/input/*.gml"` to process all GML files in the directory.

### Q: What if I get errors?

**A:** Check the Troubleshooting section above. Most common issues are:
- Missing dependencies (run `pip install -r requirements.txt`)
- Wrong file paths (use absolute paths)
- Buildings too far apart (increase threshold)

---

## 🎓 Understanding the Analysis

This project demonstrates:

1. **Network Science:** Graph-based analysis of spatial connectivity
2. **Infrastructure Planning:** Building connectivity → transportation connectivity
3. **Accessibility Analysis:** Distance and network-based accessibility metrics
4. **Computational Methods:** Automated pipeline for spatial data analysis

The methodology is applicable to:
- Transportation network optimization
- Infrastructure service planning
- Urban accessibility assessment


