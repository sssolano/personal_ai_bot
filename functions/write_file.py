import os
from pathlib import Path
from google.genai import types


def write_file(working_directory, file_path, content):
    absolute_full_path = os.path.abspath(os.path.join(working_directory)) # ^ creating absolute path
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(absolute_full_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'


schema_write_file = types.FunctionDeclaration (
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema (
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema (
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema (
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
