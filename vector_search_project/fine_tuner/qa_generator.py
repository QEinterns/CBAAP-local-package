import json
import requests
import sys
from pathlib import Path
import os


def query_ollama(prompt, domain, context='', model='llama2'):
    url = 'http://localhost:11434/api/generate'
    data = {"model": model, "stream": False, "prompt": f"[DOMAIN] {domain} [/DOMAIN] [CONTEXT] {context} [/CONTEXT] {prompt}"}
    response = requests.post(url, json=data)
    response.raise_for_status()
    followup_data = {"model": model, "stream": False, "prompt": response.json()['response'].strip() + "What is a likely follow-up question or request? Return just the text of one question or request."}
    followup_response = requests.post(url, json=followup_data)
    followup_response.raise_for_status()
    return response.json()['response'].strip(), followup_response.json()['response'].replace("\"", "").strip()


def create_validation_file(temp_file, train_file, valid_file, test_file):
    with open(temp_file, 'r') as file:
        lines = file.readlines()
    train_lines = lines[:int(len(lines) * 0.8)]
    test_lines = lines[int(len(lines) * 0.8):int(len(lines) * 0.9)]
    valid_lines = lines[int(len(lines) * 0.9):]
    with open(train_file, 'a') as file:
        file.writelines(train_lines)
    with open(valid_file, 'a') as file:
        file.writelines(valid_lines)
    with open(test_file, 'a') as file:
        file.writelines(test_lines)


def load_domain(domain_file):
    with open(domain_file, 'r') as file:
        domain = file.read().strip()
    return domain


def main(temp_file, instructions_file, train_file, valid_file, test_file, domain_file, context):
    # path = "/Users/spatra/Desktop/Movie/Architect_Chat/Dataset/"
    domain = load_domain(domain_file)
    with open(instructions_file, 'r') as file:
        instructions = json.load(file)
    cnt = 0
    for i, instruction in enumerate(instructions, start=1):
        cnt+=1
        if(cnt>3):
            break
        print(f"Processing ({i}/{len(instructions)}): {instruction}")
        answer, followup_question = query_ollama(instruction, domain, context)
        result = json.dumps({
            'text': f'<s>[INST] {instruction}[/INST] {answer}</s>[INST]{followup_question}[/INST]'
        }) + "\n"
        with open(temp_file, 'a') as file:
            file.write(result)
    create_validation_file(temp_file, train_file, valid_file, test_file)
    print("Done! Training, testing and validation JSONL files created.")
    
if __name__ == "__main__":
    # if len(sys.argv) != 7:
    #     sys.exit("Usage: python qa_generator.py <instructions.json> <train.jsonl> <valid.jsonl> <test_file> <domain_file> <context>")
    path  = os.path.dirname(os.path.abspath(__file__)) + '/'
    main(path + "temp.jsonl", path + "instructions.json", path + "train.jsonl", path + "valid.jsonl", path + "test.jsonl", path  + "prepared_data/" +  sys.argv[1] + ".txt", sys.argv[2])