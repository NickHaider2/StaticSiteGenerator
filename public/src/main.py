import os
import shutil
from copystatic import copy_files_recursive
from generatepage import generate_pages_recursive
 
destination_path = 'public/'
source_path = "../static/"

def main():

    print(f"Deleting destination directory: {destination_path}..")
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)
    
    print(f"Copying {source_path} files to {destination_path} directory...")
    copy_files_recursive(source_path, destination_path)

    generate_pages_recursive("content", "template.html", "public")


main()
