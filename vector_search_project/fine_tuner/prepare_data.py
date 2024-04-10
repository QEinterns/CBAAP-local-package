import os
import sys

from PyPDF2 import PdfReader
from m2s_converter import multiline_to_single_conv

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    # print(page.extract_text())
    for page in reader.pages:
        text += multiline_to_single_conv(page.extract_text())
    return text

def main(directory_path,save_name):
    curent_path  = os.path.dirname(os.path.abspath(__file__))
    print(curent_path)
    directory = directory_path
    output_file = curent_path + "/prepared_data/" + f"{save_name}.txt"

    with open(output_file, 'a', encoding='utf-8') as output:
        for filename in os.listdir(directory):
            if filename.endswith('.pdf'):
                print(filename)
                pdf_path = os.path.join(directory, filename)
                text = extract_text_from_pdf(pdf_path)
                output.write(text + ' ')  # Add a couple of newlines between texts for clarity

    print("Text extracted from PDFs and written to", output_file)

if __name__ == "__main__":
    directory_path = sys.argv[1]
    save_name = sys.argv[2]
    main(directory_path,save_name)