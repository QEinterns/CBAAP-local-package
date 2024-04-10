#!/bin/bash

# Install Python 3.11 using Homebrew
brew install python@3.11

# Check if Python 3.11 is available
if command -v python3.11 &>/dev/null; then
    # Create Python 3.11 virtual environment
    python3.11 -m venv cbaap_env
else
    echo "Python 3.11 is not available. Exiting."
    exit 1
fi

# Activate the virtual environment
source cbaap_env/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Install llama-cpp-python with CMAKE_ARGS
CMAKE_ARGS="-DLLAMA_METAL=on" pip install -U llama-cpp-python --no-cache-dir

# Navigate to the specified directory
cd vector_search_project/fine_tuner/mlx-examples/lora

# Install additional dependencies from requirements.txt
pip install -r requirements.txt

# Move back to the root directory
cd ../../../../

# Navigate to llama.cpp directory
cd vector_search_project/fine_tuner/llama.cpp

# Execute make
make

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Move back to the root directory
cd ../../../


# Pull latest versions
ollama pull mistral:latest
ollama pull llama2

# Exit the script
exit 0