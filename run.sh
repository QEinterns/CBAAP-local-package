#!/bin/bash

# Check if cbaap_env exists
if [ -d "cbaap_env" ]; then
    # Activate the virtual environment
    source cbaap_env/bin/activate
    
    # Run app.py
    python app.py
    
    # Deactivate the virtual environment after running the script
    deactivate
else
    echo "Virtual environment 'cbaap_env' not found. Please make sure you ran install.sh script first."
    exit 1
fi