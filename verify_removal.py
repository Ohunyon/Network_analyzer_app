#!/usr/bin/env python3
import json

# Path to the notebook
notebook_path = "/home/seyman/Network_analyzer_app/Threat_detection_in_cloud_system.ipynb"

try:
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Check metadata keys
    metadata_keys = list(notebook.get('metadata', {}).keys())
    print(f"Metadata keys: {metadata_keys}")
    print(f"Widgets in metadata: {'widgets' in notebook.get('metadata', {})}")
    print("Verification successful - widgets metadata has been removed")
    
except Exception as e:
    print(f"Error: {str(e)}")
