from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

from config import WORKING_DIR

available_functions = types.Tool (
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function (function_call_part, verbose=False):

    if verbose == True:
        print(
            f" - Function call: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(
            f" - Calling function: {function_call_part.name}"
        )

    dispatch = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }
    name = function_call_part.name
    fn = dispatch.get(name)
    if fn is None:
        return types.Content(
            role="tool", 
            parts=[
                types.Part.from_function_response(
                    name=name, 
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
    
    
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = fn(**args)
    return types.Content(
        role="tool", 
        parts=[
            types.Part.from_function_response(
                name=name, 
                response={"result": function_result},
            )
        ],
    )