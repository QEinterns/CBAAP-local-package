import json
import nltk
import os

def load_domain_knowledge(domain_file):
    with open(domain_file, 'r') as file:
        domain_knowledge = file.read()
    return domain_knowledge

def generate_instructions(domain_knowledge, context):
    instructions = []

    # Tokenize domain knowledge into sentences
    sentences = nltk.sent_tokenize(domain_knowledge)

    # Generate logical questions based on sentences
    for sentence in sentences:
        # Tokenize each sentence into words
        words = nltk.word_tokenize(sentence)
        # Tag parts of speech for each word
        tagged_words = nltk.pos_tag(words)
        # Filter out proper nouns (NNP) and gerunds (VBG)
        proper_nouns = [word for word, tag in tagged_words if tag == 'NNP']
        gerunds = [word for word, tag in tagged_words if tag == 'VBG']
        # If there are proper nouns or gerunds in the sentence, generate questions
        if proper_nouns or gerunds:
            question = f"What is the significance of {' and '.join(proper_nouns + gerunds)} in the context of {context}?"
            instructions.append(question)

    return instructions

def save_instructions(instructions, filename):
    with open(filename, 'w') as file:
        json.dump(instructions, file, indent=4)

def main(domain_file, context):
    # Specify the directory path
    current_path  = os.path.dirname(os.path.abspath(__file__))
    print(current_path)

    # Load domain knowledge from file
    domain_knowledge = load_domain_knowledge(current_path + '/prepared_data/' + domain_file + '.txt')

    # Generate instructions
    instructions = generate_instructions(domain_knowledge, context)

    # Save instructions to JSON file
    save_instructions(instructions, current_path + '/instructions.json')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python instructions.py <domain_file> <context>")
        sys.exit(1)
    nltk.download('punkt')  # Download the punkt tokenizer
    nltk.download('averaged_perceptron_tagger')  # Download the POS tagger model
    main(sys.argv[1], sys.argv[2])