#!/usr/bin/env python3
import json

# Path to the notebook
notebook_path = "/home/seyman/Network_analyzer_app/Threat_detection_in_cloud_system.ipynb"

try:
    # Read the notebook file
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)
    
    # Check if the notebook has widgets metadata
    if 'widgets' in notebook_content.get('metadata', {}):
        print("Found widgets metadata, removing it...")
        
        # Remove the widgets section from metadata
        del notebook_content['metadata']['widgets']
        
        # Write the updated notebook back to file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook_content, f, indent=2)
        
        print("Success: Removed 'widgets' from metadata")
    else:
        print("No widgets metadata found in the notebook")
        
except Exception as e:
    print(f"Error: {str(e)}")
