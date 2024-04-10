#!/bin/bash

# Define the directory containing Python files

source qef/bin/activate

FINETUNE_DIR="./fine_tuner"
# pip install nltk
# pip install PyPDF2
# pip install requests
# Check if the directory exists
if [ ! -d "$FINETUNE_DIR" ]; then
    echo "Error: 'finetune' directory does not exist."
    exit 1
fi

# Prompt the user for input for the first Python file
echo "Enter directory path:"
read user_input_1
echo "Enter the domain name: "
read additional_input
python3 "$FINETUNE_DIR/prepare_data.py" "$user_input_1"

context="$additional_input"

# Execute the second Python file with the last variable as the system argument
python3 "$FINETUNE_DIR/instructions.py" "$context" "$context"

# Execute the third Python file with the last variable passed as both system arguments
python3 "$FINETUNE_DIR/qa_generator.py" "$context" "$context"

echo "Enter number of iterations:"
read user_input_3
echo "Enter the model name to save "
read user_input_4
echo "Enter the quantization level "
read quan
python "$FINETUNE_DIR/fine_tune.py" "$user_input_3" "$user_input_4" "$quan"

MODELFILE="${FINETUNE_DIR}/modelfile"
touch "${MODELFILE}"

# Construct the path for the model file
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
model_file_path="${SCRIPT_DIR}/fine_tuner/finetune$user_input_3/$user_input_4.gguf"
echo "$model_file_path"


echo "FROM \"$model_file_path\"" > "$MODELFILE"
echo "PARAMETER stop \"<|im_start|>\"" >> "${MODELFILE}"
echo "PARAMETER stop \"<|im_end|>\"" >> "${MODELFILE}"
echo "TEMPLATE \"\"\"" >> "${MODELFILE}"
echo "<|im_start|>system" >> "${MODELFILE}"
echo "{{ .System }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>user" >> "${MODELFILE}"
echo "{{ .Prompt }}<|im_end|>" >> "${MODELFILE}"
echo "<|im_start|>assistant" >> "${MODELFILE}"
echo '"""' >> "${MODELFILE}"


ollama create automate1 -f "${MODELFILE}"

