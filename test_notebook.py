#!/usr/bin/env python3
import json
import sys

# Path to the notebook
notebook_path = "/home/seyman/Network_analyzer_app/fixed_notebook.ipynb"

try:
    # Attempt to load the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Basic validation - check if all required keys are present
    required_keys = ['cells', 'metadata', 'nbformat', 'nbformat_minor']
    missing_keys = [key for key in required_keys if key not in notebook]
    
    if missing_keys:
        print(f"Error: Notebook is missing required keys: {', '.join(missing_keys)}")
        sys.exit(1)
    
    # Check widget metadata structure
    if 'widgets' in notebook['metadata']:
        print("Widgets metadata found")
        widgets_keys = notebook['metadata']['widgets'].keys()
        print(f"Keys in widgets metadata: {', '.join(widgets_keys)}")
        
        if 'state' not in widgets_keys:
            print("Warning: 'state' key is still missing in widgets metadata!")
        else:
            print("'state' key is present in widgets metadata")
    
    print("✅ Notebook loaded and basic validation passed")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Error loading notebook: {str(e)}")
    sys.exit(1)
