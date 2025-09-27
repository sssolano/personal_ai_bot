# directory is treated as relative path within the working_directory
import os
from pathlib import Path
from google.genai import types

def get_files_info(working_directory, directory="."):
    
    # * joining the both paths 
    original_full_path = os.path.join(working_directory, directory)
    

    # * converting both into absolute paths
    absolute_path = os.path.abspath(original_full_path)
    absolute_working_directory = os.path.abspath(working_directory)

    if not absolute_path.startswith(absolute_working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(absolute_path):
        return f'Error: "{directory}" is not a directory'

    try:
        my_list = []
        for file_name in os.listdir(absolute_path):
            full_path = os.path.join(absolute_path, file_name)
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            my_list.append(f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(my_list)
    except Exception as e:
        return f'Error: {str(e)}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

