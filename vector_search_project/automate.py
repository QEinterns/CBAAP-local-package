import os
import subprocess
import shutil
import re

def delete_finetune_folders(directory):
    pattern = re.compile(r'finetune\d+')
    for item in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, item)):
            if pattern.match(item):
                folder_path = os.path.join(directory, item)
                print(f"Deleting folder: {folder_path}")
                try:
                    shutil.rmtree(folder_path)
                    print(f"Folder '{item}' deleted successfully.")
                except OSError as e:
                    print(f"Error: {e.strerror}")



def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)  # remove the file
                print(f"File '{filename}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def remove_adapter(directory, filename):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f"File '{filename}' removed successfully.")
        except OSError as e:
            print(f"Error: {e.strerror}")


def clear_jsonl_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".jsonl"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "w") as file:
                    file.truncate(0)  # Truncate the file to clear its contents
                print(f"Contents of '{filename}' cleared successfully.")
            except Exception as e:
                print(f"Error: {e}")


def run_script(pdf_path, context, iteration_count, final_model_name, quan,model_name):
    current_directory = os.getcwd()
    print(current_directory)
   


    delete_finetune_folders(os.path.join(current_directory, "vector_search_project/fine_tuner"))
    clear_directory(os.path.join(current_directory, "uploaded_pdfs"))
    clear_directory(os.path.join(current_directory, "vector_search_project/fine_tuner/prepared_data"))
    remove_adapter(current_directory,'adapters.npz')
    clear_jsonl_files(os.path.join(current_directory, "vector_search_project/fine_tuner"))

    # Define the directory containing Python files
    FINETUNE_DIR = os.path.join(current_directory, "vector_search_project/fine_tuner")

    # Activate the virtual environment

    # Check if the directory exists
    if not os.path.isdir(FINETUNE_DIR):
        print("Error: 'finetune' directory does not exist.")
        return

    # Execute prepare_data.py
    prepare_data_command = f"python {FINETUNE_DIR}/prepare_data.py {pdf_path} {context}"
    subprocess.run(prepare_data_command, shell=True)

    context = context

    # Execute instructions.py
    instructions_command = f"python {FINETUNE_DIR}/instructions.py {context} {context}"
    subprocess.run(instructions_command, shell=True)

    # Execute qa_generator.py
    qa_generator_command = f"python {FINETUNE_DIR}/qa_generator.py {context} {context}"
    subprocess.run(qa_generator_command, shell=True)

    # Execute fine_tune.py
    fine_tune_command = f"python {FINETUNE_DIR}/fine_tune.py {iteration_count} {final_model_name} {quan} {model_name}"
    subprocess.run(fine_tune_command, shell=True)

    # # Create and populate the model file
    MODELFILE = f"{FINETUNE_DIR}/modelfile"
    open(MODELFILE, 'w').close()  # Clear the file

    with open(MODELFILE, 'a') as f:
        model_file_path = f"{FINETUNE_DIR}/finetune{iteration_count}/{final_model_name}.gguf"
        f.write(f"FROM \"{model_file_path}\"\n")
        f.write("PARAMETER stop \"<|im_start|>\"\n")
        f.write("PARAMETER stop \"<|im_end|>\"\n")
        f.write("TEMPLATE \"\"\"\n")
        f.write("<|im_start|>system\n")
        f.write("{{ .System }}<|im_end|>\n")
        f.write("<|im_start|>user\n")
        f.write("{{ .Prompt }}<|im_end|>\n")
        f.write("<|im_start|>assistant\n")
        f.write('"""\n')

    # Execute ollama create command
    ollama_command = f"ollama create {final_model_name} -f {MODELFILE}"
    subprocess.run(ollama_command, shell=True)


# run_script('/Users/nishanth/local_finetune/uploaded_pdfs', 'task', "1", "nishu",'Q5_0','mistral 7B')