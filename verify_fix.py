#!/usr/bin/env python3
import json

# Load the notebook
with open('/home/seyman/Network_analyzer_app/Threat_detection_in_cloud_system.ipynb', 'r') as f:
    notebook = json.load(f)

# Check and print widgets metadata structure
if 'widgets' in notebook['metadata']:
    print("Widgets metadata found")
    print("Keys in widgets metadata:", list(notebook['metadata']['widgets'].keys()))
    
    if 'state' in notebook['metadata']['widgets']:
        print("'state' key found in widgets metadata")
    else:
        print("'state' key is still missing!")
else:
    print("No widgets metadata found")
