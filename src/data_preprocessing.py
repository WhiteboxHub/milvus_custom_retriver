import PyPDF2
import os



def get_pdf_paths(pdf_folder : str) -> list[str]:
    
    paths = {}
    files = os.listdir(pdf_folder)
    for file in files:
        if file.endswith('.pdf'):
            paths[file] = f'{pdf_folder}/{file}'
    print(paths)
    return paths


def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path,'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


