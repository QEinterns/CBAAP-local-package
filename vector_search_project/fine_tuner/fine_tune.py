import os
import subprocess
import sys
import shutil

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode()

def main(num_iterations,model_name,quan,finetune_model):
    activate_command = "source activate testenv"
    subprocess.run(activate_command, shell=True)

    current_directory = os.getcwd()
    adapter_directory = current_directory
    current_directory = os.path.join(current_directory, "vector_search_project")
    print(current_directory)
    
    fine_tuner_directory = os.path.join(current_directory, "fine_tuner")
    lora_script = os.path.join(fine_tuner_directory, "mlx-examples", "lora", "lora.py")
    fuse_script = os.path.join(fine_tuner_directory, "mlx-examples", "lora", "fuse.py")
    llama_script_convert = os.path.join(fine_tuner_directory, "llama.cpp", "convert.py")
    llama_script_quantize = os.path.join(fine_tuner_directory, "llama.cpp")

    fine_name = "mistralai/Mistral-7B-Instruct-v0.2"
    # if("mistral" in finetune_model):
    #     if("7B" in finetune_model):
    #         fine_name = "mistralai/Mistral-7B-Instruct-v0.2"
    #     else:
    #         fine_name = "mistralai/Mistral-13B-Instruct-v0.2"
    # else:
    #     fine_name = "TheBloke/Llama-2-7B-GGML"

    # if finetune_model[0]=='l' or finetune_model[0]=='L':
    #     fine_name = "TheBloke/Llama-2-7B-GGML"
        
    print("reaching")
    command = f"python {lora_script} --train --model {fine_name} --data {fine_tuner_directory} --batch-size 1 --lora-layers 1 --iters 1"
    print(command)
    a  = execute_command(command)
    print(a)


    command = f"python {fuse_script} --model {fine_name} --adapter-file {adapter_directory}/adapters.npz --save-path {fine_tuner_directory}/finetune1"
    print(command)
    a = execute_command(command)
    print(a)

    # Loop for remaining iterations
    for i in range(2, num_iterations + 1):

        command = f"python {lora_script} --train --model {fine_tuner_directory}/finetune{i - 1} --data {fine_tuner_directory} --batch-size 1 --lora-layers 1 --iters 10"
        a = execute_command(command)
        print(a)

        command = f"python {fuse_script} --model {fine_tuner_directory}/finetune{i - 1} --adapter-file {adapter_directory}/adapters.npz --save-path {fine_tuner_directory}/finetune{i}"
        a = execute_command(command)
        print(a)


        
        os.remove(f"{adapter_directory}/adapters.npz")
        shutil.rmtree(f"{fine_tuner_directory}/finetune{i-1}")

    
    command = f"python {llama_script_convert} --outtype f16 --ctx 4096 {fine_tuner_directory}/finetune{num_iterations}"
    execute_command(command)

    command_s = f"{llama_script_quantize}/quantize  {fine_tuner_directory}/finetune{num_iterations}/ggml-model-f16.gguf {fine_tuner_directory}/finetune{num_iterations}/{model_name}.gguf {quan}"
    subprocess.run(command_s, shell=True)



if __name__ == "__main__":
    num_iterations = int(sys.argv[1])
    model_name = sys.argv[2]
    quan  = sys.argv[3]
    finetune_model = sys.argv[4]
    main(num_iterations, model_name,quan,finetune_model)
