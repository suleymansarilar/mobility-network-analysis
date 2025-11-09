# Adım 1 ve 2 Özeti - Building Extraction & Network Construction

## ✅ Tamamlananlar

### Adım 1: CityGML Parser
- **Dosya:** `utils/gml_parser.py`
- **Script:** `scripts/1_extract_buildings.py`

**Ne yapıyor:**
1. CityGML dosyasını parse eder
2. Her building'in footprint'ini çıkarır (ground surface polygon)
3. Building metadata'sını extract eder (ID, centroid, area, height, type)
4. Coordinate system'i detect eder ve gerekirse transform eder
5. CSV dosyasına kaydeder

**Özellikler:**
- Multiple CityGML schema versiyonlarını destekler
- WGS84 (lat/lon) ve projected coordinate system'leri handle eder
- Ground surface extraction (lod0FootPrint, lod1FootPrint)
- Polygon validation ve fixing (self-intersection düzeltme)
- Error handling ve logging

**Kullanım:**
```bash
python scripts/1_extract_buildings.py --input data/input/sample_buildings.gml --output data/processed/buildings_geodata.csv
```

**Çıktılar:**
- `buildings_geodata.csv`: Building data (ID, centroid, area, height, type)
- `buildings_geodata_footprints.pkl`: Building footprints (Shapely Polygon'lar)

---

### Adım 2: Network Graph Construction
- **Dosya:** `utils/network_utils.py`
- **Script:** `scripts/2_build_network.py`

**Ne yapıyor:**
1. Building'ler arası mesafeleri hesaplar (Haversine veya Euclidean)
2. Network graph oluşturur (NetworkX)
3. Edge'leri threshold'a göre ekler
4. Network statistics hesaplar

**Özellikler:**
- **Distance-based method:** Threshold içindeki building'leri connect eder
- **Delaunay triangulation method:** Nearest neighbors'ı connect eder
- **Haversine distance:** Lat/lon için doğru mesafe hesaplama
- **Edge-to-edge distance:** Centroid yerine polygon edge distance (daha doğru)
- Network statistics: density, clustering, shortest path length

**Kullanım:**
```bash
python scripts/2_build_network.py --input data/processed/buildings_geodata.csv --output data/processed/building_network_graph.pkl --threshold 200
```

**Çıktılar:**
- `building_network_graph.pkl`: NetworkX graph (pickle)
- `building_network_graph_stats.json`: Network statistics
- `building_network_graph_edges.csv`: Edge list (source, target, distance)

---

## 📊 Data Flow

```
CityGML File (.gml)
    ↓
[Adım 1] CityGML Parser
    ↓
buildings_geodata.csv + footprints.pkl
    ↓
[Adım 2] Network Builder
    ↓
building_network_graph.pkl + stats.json + edges.csv
```

---

## 🧪 Test Etmek İçin

### 1. Sample CityGML Dosyası Hazırlama

Eğer CityGML dosyanız yoksa, basit bir sample oluşturabiliriz:

```python
# scripts/create_sample_gml.py (oluşturulacak)
```

Veya mevcut CityGML dosyanızı kullanın.

### 2. Pipeline'ı Test Et

```bash
# Adım 1
python scripts/1_extract_buildings.py --input data/input/your_file.gml --output data/processed/buildings_geodata.csv

# Adım 2
python scripts/2_build_network.py --input data/processed/buildings_geodata.csv --output data/processed/building_network_graph.pkl --threshold 200
```

### 3. Sonuçları Kontrol Et

```python
import pandas as pd
import pickle
import networkx as nx

# Buildings
df = pd.read_csv('data/processed/buildings_geodata.csv')
print(df.head())

# Network graph
with open('data/processed/building_network_graph.pkl', 'rb') as f:
    G = pickle.load(f)

print(f"Nodes: {G.number_of_nodes()}")
print(f"Edges: {G.number_of_edges()}")
print(f"Density: {nx.density(G):.4f}")
```

---

## 🔍 Detaylı Açıklamalar

### CityGML Parser Detayları

**Namespace Handling:**
- CityGML 2.0 namespace'lerini destekler
- `bldg:Building`, `bldg:GroundSurface`, `gml:Polygon` elementlerini parse eder

**Coordinate Extraction:**
- `gml:posList`: Space-separated coordinates (2D veya 3D)
- `gml:pos`: Individual points
- 3D coordinates'tan 2D'ye dönüşüm (z değeri atlanır)

**Polygon Validation:**
- Self-intersection kontrolü
- Invalid polygon'ları `buffer(0)` ile düzeltir
- Minimum 3 point kontrolü

### Network Construction Detayları

**Distance Calculation:**
- **Haversine:** Great-circle distance (lat/lon için doğru)
- **Euclidean:** Straight-line distance (projected coordinates için)
- **Edge-to-edge:** Polygon distance (en doğru, ama yavaş)

**Edge Creation Strategies:**
1. **Distance-based (basit):**
   - Tüm building çiftleri arası mesafe
   - Threshold içindekiler connect edilir
   - O(n²) complexity

2. **Delaunay (daha gerçekçi):**
   - Nearest neighbors'ı connect eder
   - Daha sparse graph
   - O(n log n) complexity

**Graph Properties:**
- **Undirected:** Building A → B = Building B → A
- **Weighted:** Edge weight = distance (meters)
- **Connected:** Tüm nodes birbirine erişilebilir mi?

---

## ❓ Sık Sorulan Sorular

### 1. CityGML dosyam yok, ne yapmalıyım?
- Sample CityGML oluşturabiliriz
- Veya mevcut projelerinizden CityGML export edebilirsiniz
- OpenStreetMap'ten building data çekebiliriz (alternatif)

### 2. Coordinate system farklıysa ne olur?
- Parser otomatik detect eder
- WGS84'e transform eder (gerekirse)
- Area hesaplaması için projected CRS kullanılmalı (şu an basit)

### 3. Threshold değeri nasıl belirlenmeli?
- **100m:** Çok yakın building'ler (dense urban)
- **200m:** Normal walking distance
- **500m:** Extended walking distance
- Test ederek en uygun değeri bulun

### 4. Delaunay vs Distance-based hangisini kullanmalıyım?
- **Distance-based:** Daha dense graph, tüm yakın building'ler connect
- **Delaunay:** Daha sparse graph, sadece nearest neighbors
- İkisini de test edip karşılaştırın

---

## 📝 Sonraki Adımlar

### Adım 3: Network Analysis
- Shortest path algorithms (Dijkstra)
- Centrality metrics (betweenness, closeness, PageRank)
- Network statistics

### Adım 4: Accessibility Scoring
- Distance-based accessibility
- Network-based accessibility
- Weighted accessibility

### Adım 5: Visualization
- Network graph visualization
- Accessibility heatmap
- Interactive maps

---

## 🐛 Bilinen Sorunlar / İyileştirmeler

1. **Area calculation:** Projected CRS kullanılmalı (şu an source CRS'te)
2. **Large datasets:** O(n²) complexity için optimization gerekebilir
3. **Road network:** Road data entegrasyonu yok (şu an)
4. **3D analysis:** Height bilgisi kullanılmıyor (şu an)

---

## 💡 İpuçları

1. **Test data:** Küçük bir CityGML dosyası ile başlayın (5-10 building)
2. **Threshold tuning:** Farklı threshold değerleri deneyin
3. **Visualization:** Adım 2'den sonra graph'ı visualize edin (matplotlib)
4. **Logging:** Log dosyalarını kontrol edin (hata ayıklama için)

---

## 📚 Referanslar

- CityGML Specification: https://www.ogc.org/standards/citygml
- NetworkX Documentation: https://networkx.org/
- Shapely Documentation: https://shapely.readthedocs.io/
- Haversine Formula: https://en.wikipedia.org/wiki/Haversine_formula

