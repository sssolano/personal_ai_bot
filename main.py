import os 
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions
from call_function import call_function, available_functions


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


    for i in range(20):
        final_text = generate_content(client, messages, verbose)
        if final_text:
            print("Final response:")
            print(final_text)
            break
    else:
        print("Stopped after 20 iterations.")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt,
        ),
    )
    
    for candidate in response.candidates:
        messages.append(candidate.content)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls:
        return response.text


    for function_call_part in response.function_calls:
        if verbose:
            print(f"-> Calling Function : {function_call_part.name}")
        result_content = call_function(function_call_part, verbose)
        
        if (not result_content.parts 
            or not result_content.parts[0].function_response):
            raise Exception("Empty function call result")
        

        tool_msg = types.Content(
            role='user',
            parts=result_content.parts
        )
        messages.append(tool_msg)

    return None


if __name__ == "__main__":
    main()