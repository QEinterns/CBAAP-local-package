#!/bin/bash

# Define the directory containing Python files
source qef/bin/activate

FINETUNE_DIR="./fine_tuner"

# Check if the directory exists
if [ ! -d "$FINETUNE_DIR" ]; then
    echo "Error: 'finetune' directory does not exist."
    exit 1
fi

# Read input values from arguments
user_input_1="$1"  # Directory path
additional_input="$2"  # Domain name (context)
user_input_3="$3"  # Number of iterations
user_input_4="$4"  # Model name to save
quan="$5"  # Quantization level
finetune_model="$6" #final_model name


# Prepare data using the provided directory path
python3 "$FINETUNE_DIR/prepare_data.py" "$user_input_1"

# Execute instructions.py with the provided context
python3 "$FINETUNE_DIR/instructions.py" "$additional_input" "$additional_input"

# Execute qa_generator.py with the provided context
python3 "$FINETUNE_DIR/qa_generator.py" "$additional_input" "$additional_input"

# Fine tune the model with the provided number of iterations, model name, and quantization level
python "$FINETUNE_DIR/fine_tune.py" "$user_input_3" "$user_input_4" "$quan" "$finetune_model"

MODELFILE="${FINETUNE_DIR}/modelfile"
touch "${MODELFILE}"

# Construct path for the model file
model_file_path="${FINETUNE_DIR}/finetune${user_input_3}/${user_input_4}.gguf"

# Write content to model file
echo "FROM \"$model_file_path\"" > "$MODELFILE"
echo "PARAMETER stop \"\"" >> "${MODELFILE}"
echo "PARAMETER stop \"\"" >> "${MODELFILE}"
echo "TEMPLATE \"\"\"" >> "${MODELFILE}"
echo "system" >> "${MODELFILE}"
echo "{{ .System }}" >> "${MODELFILE}"
echo "user" >> "${MODELFILE}"
echo "{{ .Prompt }}" >> "${MODELFILE}"
echo "assistant" >> "${MODELFILE}"
echo '"""' >> "${MODELFILE}"

# Create automate1 with ollama
ollama create finale1 -f "${MODELFILE}"
