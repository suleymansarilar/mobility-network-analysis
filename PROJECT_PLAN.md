# CityGML → Mobility Network Analysis - Proje Planı

## 🎯 Proje Hedefi

CityGML verilerinden building connectivity network'i çıkararak, transportation/mobility network analysis kavramlarını göstermek. WPI Dr. Lindsay Graff'ın araştırma alanlarına (network optimization, infrastructure planning) uygun bir demo projesi.

---

## 📋 Proje Yapısı

```
mobility-network-analysis/
├── README.md                          # Ana proje açıklaması
├── requirements.txt                   # Python dependencies
├── PROJECT_PLAN.md                    # Bu dosya (detaylı plan)
├── data/
│   ├── input/                         # CityGML input dosyaları
│   │   └── sample_buildings.gml
│   ├── processed/                     # İşlenmiş veriler
│   │   ├── buildings_geodata.csv      # Building footprints (lat/lon, area, centroid)
│   │   ├── building_network_graph.pkl # NetworkX graph (pickle)
│   │   └── network_metrics.csv        # Centrality, accessibility metrics
│   └── output/                        # Final çıktılar
│       ├── network_graph.png          # Network visualization
│       ├── accessibility_heatmap.png  # Accessibility heatmap
│       ├── network_analysis_report.md # Analiz raporu
│       └── optimal_paths.json         # Shortest paths between buildings
├── scripts/
│   ├── 1_extract_buildings.py         # CityGML → Building footprints
│   ├── 2_build_network.py             # Buildings → Network graph
│   ├── 3_analyze_network.py           # Network metrics, shortest paths
│   ├── 4_calculate_accessibility.py   # Accessibility scoring
│   ├── 5_visualize_network.py         # Graph + heatmap visualization
│   └── run_pipeline.py                # Tüm pipeline'ı çalıştır
├── utils/
│   ├── gml_parser.py                  # CityGML parsing utilities
│   ├── network_utils.py               # Network analysis utilities
│   └── visualization_utils.py         # Visualization helpers
└── tests/
    ├── test_gml_parser.py
    ├── test_network_builder.py
    └── test_accessibility.py
```

---

## 🔄 İş Akışı (Pipeline)

### Adım 1: CityGML Parsing → Building Footprints
**Script:** `1_extract_buildings.py`

**Input:**
- CityGML dosyası (.gml)

**Process:**
1. CityGML dosyasını parse et (lxml veya pycitygml)
2. Her building'in footprint'ini çıkar (ground surface polygon)
3. Building metadata'sını extract et:
   - Building ID
   - Centroid coordinates (lat/lon)
   - Ground surface area
   - Height (if available)
   - Building type/usage (if available)

**Output:**
- `buildings_geodata.csv` (columns: building_id, centroid_lat, centroid_lon, area_m2, height_m, building_type)

**Teknik Detaylar:**
- CityGML schema: `bldg:Building`, `bldg:GroundSurface`
- Coordinate system: WGS84 (EPSG:4326) veya local projection
- Polygon extraction: `bldg:GroundSurface` → Shapely Polygon

---

### Adım 2: Network Graph Construction
**Script:** `2_build_network.py`

**Input:**
- `buildings_geodata.csv`

**Process:**
1. Building'ler arası mesafeleri hesapla (centroid-to-centroid veya edge-to-edge)
2. Network graph oluştur (NetworkX):
   - **Nodes:** Buildings (node_id = building_id)
   - **Edges:** Connectivity between buildings
   - **Edge weights:** Distance (meters) veya travel time (estimated)

**Edge Creation Strategies:**
- **Strategy 1: Distance-based** (basit)
  - Tüm building çiftleri arası mesafe hesapla
  - Threshold belirle (örn: 200m içindeki building'ler connected)
  
- **Strategy 2: Voronoi/Delaunay** (daha gerçekçi)
  - Delaunay triangulation ile nearest neighbors
  - Sadece komşu building'leri connect et
  
- **Strategy 3: Road-aware** (en gerçekçi, ama road data gerekir)
  - Road network'i kullan (OpenStreetMap veya DXF)
  - Sadece road ile bağlantılı building'leri connect et

**Başlangıç için:** Strategy 1 (distance-based) kullan, sonra Strategy 2'ye geçebiliriz.

**Output:**
- `building_network_graph.pkl` (NetworkX graph, pickle format)
- `network_edges.csv` (edge list: source, target, distance_m, weight)

**Teknik Detaylar:**
- Distance calculation: Haversine formula (lat/lon) veya Euclidean (projected coordinates)
- Graph type: Undirected weighted graph
- Edge weight: Distance in meters (veya normalized 0-1)

---

### Adım 3: Network Analysis
**Script:** `3_analyze_network.py`

**Input:**
- `building_network_graph.pkl`

**Process:**
1. **Shortest Path Analysis:**
   - Tüm node çiftleri arası shortest path hesapla (Dijkstra)
   - Path length (distance) ve path (node sequence) kaydet

2. **Centrality Metrics:**
   - **Degree Centrality:** Her node'un kaç edge'i var
   - **Betweenness Centrality:** Node'un kaç shortest path'te geçtiği
   - **Closeness Centrality:** Node'un diğer tüm node'lara ortalama uzaklığı
   - **PageRank:** Importance score (optional)

3. **Network Statistics:**
   - Total nodes, edges
   - Average degree
   - Network density
   - Average shortest path length
   - Clustering coefficient

**Output:**
- `network_metrics.csv` (columns: building_id, degree, betweenness, closeness, pagerank)
- `optimal_paths.json` (shortest paths between all pairs)
- `network_stats.json` (overall network statistics)

**Teknik Detaylar:**
- NetworkX functions: `shortest_path()`, `betweenness_centrality()`, `closeness_centrality()`
- Large networks için: Approximate algorithms (örn: betweenness için sampling)

---

### Adım 4: Accessibility Scoring
**Script:** `4_calculate_accessibility.py`

**Input:**
- `building_network_graph.pkl`
- `buildings_geodata.csv`

**Process:**
1. **Distance-based Accessibility:**
   - Her building için, X metre (örn: 500m) içindeki building sayısı
   - Cumulative opportunity score

2. **Network-based Accessibility:**
   - Her building için, network üzerinden erişilebilen building sayısı
   - Average shortest path distance to all other buildings

3. **Weighted Accessibility:**
   - Building area'ya göre ağırlıklandırılmış accessibility
   - Büyük building'ler daha "important" kabul edilir

**Output:**
- `accessibility_metrics.csv` (columns: building_id, distance_500m_count, network_reachable_count, avg_path_distance, weighted_accessibility)

**Teknik Detaylar:**
- Distance threshold: 500m (walkable distance)
- Network reachability: BFS veya shortest path algorithm
- Weight calculation: Building area / total area

---

### Adım 5: Visualization
**Script:** `5_visualize_network.py`

**Input:**
- `building_network_graph.pkl`
- `buildings_geodata.csv`
- `network_metrics.csv`
- `accessibility_metrics.csv`

**Process:**
1. **Network Graph Visualization:**
   - Nodes: Buildings (position = centroid lat/lon)
   - Edges: Connections (color = distance, thickness = weight)
   - Node size: Degree centrality veya building area
   - Node color: Betweenness centrality veya accessibility score

2. **Accessibility Heatmap:**
   - Building'leri map üzerinde göster
   - Color scale: Accessibility score (low = blue, high = red)
   - Interpolation: Kriging veya IDW (optional)

3. **Optimal Path Highlighting:**
   - Seçili building çiftleri arası shortest path'leri highlight et
   - Path'i kalın çizgi ile göster

**Output:**
- `network_graph.png` (network visualization)
- `accessibility_heatmap.png` (accessibility heatmap)
- `network_interactive.html` (optional: Plotly interactive map)

**Teknik Detaylar:**
- Library: Matplotlib + NetworkX (static) veya Plotly (interactive)
- Basemap: OpenStreetMap (contextily) veya CartoDB
- Coordinate projection: Web Mercator (EPSG:3857) for web maps

---

### Adım 6: Pipeline Runner
**Script:** `run_pipeline.py`

**Function:**
- Tüm adımları sırayla çalıştır
- Error handling ve logging
- Progress bar göster
- Config file support (thresholds, parameters)

**Usage:**
```bash
python scripts/run_pipeline.py --input data/input/sample_buildings.gml --output data/output/
```

---

## 📊 Beklenen Çıktılar

### 1. Network Graph Visualization
- Building'ler nodes olarak
- Connections edges olarak
- Node size/color: Centrality metrics
- Edge thickness: Distance/weight

### 2. Accessibility Heatmap
- Building'ler map üzerinde
- Color: Accessibility score
- Legend: Score range

### 3. Network Analysis Report
- Network statistics (nodes, edges, density, etc.)
- Top 10 most central buildings
- Top 10 most accessible buildings
- Shortest paths örnekleri
- Transportation network analysis açıklaması

### 4. Data Files
- CSV files: Buildings, metrics, accessibility
- JSON files: Network stats, optimal paths
- Pickle files: NetworkX graph (for further analysis)

---

## 🛠️ Teknik Gereksinimler

### Python Libraries:
- `lxml` veya `pycitygml`: CityGML parsing
- `shapely`: Geometric operations (polygons, distances)
- `geopandas`: Geospatial data handling
- `networkx`: Network analysis
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `matplotlib`: Static visualization
- `plotly`: Interactive visualization (optional)
- `contextily`: Basemap tiles (optional)
- `scipy`: Spatial analysis (optional)

### Data Requirements:
- CityGML file with multiple buildings
- Coordinate system: WGS84 (lat/lon) veya local projection
- Building footprints: Ground surface polygons

---

## 📝 Sonraki Adımlar

1. **Adım 1'i başlat:** CityGML parser'ı yaz
2. **Test data hazırla:** Sample CityGML file
3. **Her adımı sırayla implement et**
4. **Test ve debug**
5. **Visualization'ı iyileştir**
6. **Documentation'ı tamamla**

---

## 🎓 WPI Bağlantısı

Bu proje şunları gösterir:
- **Network optimization:** Shortest path algorithms, centrality metrics
- **Infrastructure planning:** Building connectivity, accessibility analysis
- **Computational methods:** Scalable pipeline, automated analysis
- **Transportation network concepts:** Graph-based thinking, multi-modal systems (building connectivity → transportation connectivity)

---

## 📅 Timeline

- **Hafta 1:**
  - Adım 1-2: CityGML parsing + Network construction
  - Test data hazırlama
  - Basic visualization

- **Hafta 2:**
  - Adım 3-4: Network analysis + Accessibility
  - Advanced visualization
  - Documentation
  - Report writing

---

## ❓ Sorular

1. **CityGML dosyası hazır mı?** Yoksa sample data mı oluşturalım?
2. **Coordinate system:** WGS84 mi, local projection mu?
3. **Edge strategy:** Distance-based mi, Delaunay mi?
4. **Visualization:** Static (matplotlib) mi, interactive (plotly) mi?

