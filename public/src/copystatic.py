import os
import shutil

def copy_files_recursive(source_path, destination_path):
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)
        print(f"Path created: {destination_path}")
    
    for file in os.listdir(source_path):

        content_src_path = os.path.join(source_path, file)
        content_dest_path = os.path.join(destination_path, file)

        print(f"Copying {content_src_path} to {destination_path}")
        if os.path.isfile(content_src_path):
            shutil.copy(content_src_path, content_dest_path)
        else: 
            copy_files_recursive(content_src_path, content_dest_path)