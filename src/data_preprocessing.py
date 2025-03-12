
import os



def get_pdf_paths(pdf_folder : str) -> list[str]:
    
    paths = {}
    files = os.listdir(pdf_folder)
    for file in files:
        if file.endswith('.pdf'):
            paths[file] = f'{pdf_folder}/{file}'
    print(paths)
    return paths

