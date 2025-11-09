"""
Test script for Adım 1 and 2
Tests the pipeline with Turkish GML files
"""

import sys
import os
import subprocess
from pathlib import Path

# Add scripts to path
sys.path.append(str(Path(__file__).parent))

# Import using importlib to handle numeric module names
import importlib.util

def load_module(module_path, module_name):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load modules
extract_module = load_module(
    Path(__file__).parent / "scripts" / "1_extract_buildings.py",
    "extract_buildings"
)
network_module = load_module(
    Path(__file__).parent / "scripts" / "2_build_network.py",
    "build_network"
)

extract_buildings = extract_module.extract_buildings
build_network = network_module.build_network

def main():
    """Test the pipeline with GML files."""
    
    # GML files directory
    gml_dir = Path(r"C:\mobility-network-analysis\gml_files")
    output_dir = Path(r"C:\mobility-network-analysis\data")
    
    # Create output directories
    (output_dir / "processed").mkdir(parents=True, exist_ok=True)
    (output_dir / "output").mkdir(parents=True, exist_ok=True)
    
    # Find all GML files
    gml_files = list(gml_dir.glob("*.gml"))
    
    if not gml_files:
        print(f"No GML files found in {gml_dir}")
        return
    
    print(f"Found {len(gml_files)} GML files")
    
    # Process each GML file
    all_buildings = []
    
    for gml_file in gml_files:
        print(f"\n{'='*60}")
        print(f"Processing: {gml_file.name}")
        print(f"{'='*60}")
        
        # Adım 1: Extract buildings
        output_csv = output_dir / "processed" / f"{gml_file.stem}_buildings.csv"
        
        try:
            df = extract_buildings(str(gml_file), str(output_csv))
            if df is not None and not df.empty:
                all_buildings.append(df)
                print(f"[OK] Extracted {len(df)} buildings from {gml_file.name}")
            else:
                print(f"[FAIL] No buildings extracted from {gml_file.name}")
        except Exception as e:
            print(f"[ERROR] Error processing {gml_file.name}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Combine all buildings
    if all_buildings:
        import pandas as pd
        combined_df = pd.concat(all_buildings, ignore_index=True)
        combined_csv = output_dir / "processed" / "all_buildings.csv"
        combined_df.to_csv(combined_csv, index=False)
        print(f"\n{'='*60}")
        print(f"Combined {len(combined_df)} buildings from {len(all_buildings)} files")
        print(f"Saved to: {combined_csv}")
        
        # Adım 2: Build network
        print(f"\n{'='*60}")
        print("Adım 2: Building Network Graph")
        print(f"{'='*60}")
        
        output_graph = output_dir / "processed" / "building_network_graph.pkl"
        
        try:
            G = build_network(
                str(combined_csv),
                str(output_graph),
                distance_threshold=200.0,
                method='distance',
                use_edge_distance=False
            )
            print(f"[OK] Network graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        except Exception as e:
            print(f"[ERROR] Error building network: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n[FAIL] No buildings extracted. Cannot build network.")

if __name__ == '__main__':
    main()

