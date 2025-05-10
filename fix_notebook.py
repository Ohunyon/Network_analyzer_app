#!/usr/bin/env python3
import json

# Path to the notebook
notebook_path = "/home/seyman/Network_analyzer_app/Threat_detection_in_cloud_system.ipynb"

# Read the notebook file
with open(notebook_path, 'r', encoding='utf-8') as f:
    notebook_content = json.load(f)

# Check if the notebook has widgets metadata
if 'widgets' in notebook_content.get('metadata', {}):
    print("Found widgets metadata")
    
    # Check if state key is missing
    if 'state' not in notebook_content['metadata']['widgets']:
        print("'state' key is missing in widgets metadata, adding it...")
        
        # Add empty state object
        notebook_content['metadata']['widgets']['state'] = {}
        
        # Write the updated notebook back to file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2)
        
        print("Fixed: Added 'state' key to widgets metadata")
    else:
        print("The notebook already has a 'state' key in widgets metadata")
else:
    print("No widgets metadata found in the notebook")
