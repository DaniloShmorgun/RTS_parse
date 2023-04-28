import os
from pathlib import Path

class FilesFunctions:
    @staticmethod
    def get_project_root():
        current_dir = os.path.abspath(os.curdir)
        while not (os.path.isfile(os.path.join(current_dir, 'setup.py'))):
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                # Reached the root directory without finding any project indicators
                raise Exception("Project root not found.")
            current_dir = parent_dir
        return current_dir
    
    @staticmethod
    def clear_file(filename : str) -> None:
        with open(filename, 'w') as file:
            pass
    
    def get_file_names_from_folder(folder):
        
        folder_path = Path(folder)  # Replace with the path to your folder

        for file_path in folder_path.iterdir():
            if file_path.is_file():
                print(file_path.name)



