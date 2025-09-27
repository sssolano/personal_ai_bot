import os
import subprocess
import sys
from pathlib import Path
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    path_wd = Path(working_directory).resolve()
    target = (path_wd / file_path).resolve()

    if not target.is_relative_to(path_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not target.exists():
        return f'Error: File "{file_path}" not found.'

    if not target.suffix == '.py':
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmd = [sys.executable, target, *args]
        completed_process = subprocess.run(cmd, cwd=path_wd, capture_output=True, text=True, timeout=30)

        if not completed_process.stdout and not completed_process.stderr:
            return f'No output produced.'

        parts = []
        
        out = f'STDOUT:{completed_process.stdout}'.rstrip()
        err = f'STDERR:{completed_process.stderr}'.rstrip()

        # No fucking clue what does this do
        if out: parts.append(out)
        if err: parts.append(err)

        if completed_process.returncode != 0:
            return f'Process exited with code: {completed_process.returncode}'

        # No idea how does this works
        return '\n'.join(parts)
    
    except Exception as e:
        return f'Error: executing Python file: {e}'



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)