import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types as genai_types

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if len(sys.argv) < 2:
        print("Please provide a prompt.")
        sys.exit(1)

    verbose = len(sys.argv) == 3 and sys.argv[2] in ("--verbose", "-v")
    user_prompt = sys.argv[1]

    working_directory = "./calculator"

    TOOL_DISPATCH = {
        "get_files_info":   lambda args: get_files_info(working_directory, **args),
        "get_file_content": lambda args: get_file_content(working_directory, **args),
        "write_file":       lambda args: write_file(working_directory, **args),
        "run_python_file":  lambda args: run_python_file(working_directory, **args),
    }

    system_instruction = (
        "You are a coding agent with access to a sandboxed working directory. \n"
        "You can read files, write files, list directories, and run Python scripts. \n"
        "Use your tools to understand and modify the codebase to fulfill the user's request. \n"
        "Think step by step: explore first, then make targeted changes, then verify by running tests or the relevant "
        "script. \n"
        "All paths you provide should be relative to the working directory. You do not need to specify the working "
        "directory in your function calls as it is automatically injected for security reasons."
    )

    messages = [
        genai_types.Content(role="user", parts=[genai_types.Part(text=user_prompt)])
    ]

    available_functions = genai_types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    config = genai_types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_instruction,
    )

    client = genai.Client(api_key=api_key)

    while True:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=messages,
            config=config,
        )

        candidate = response.candidates[0]
        messages.append(candidate.content)

        function_calls = [p for p in candidate.content.parts if p.function_call]
        if not function_calls:
            print(response.text)
            break

        tool_response_parts = []
        for part in function_calls:
            fc = part.function_call
            if verbose:
                print(f"[tool] {fc.name}({dict(fc.args)})")
            fn = TOOL_DISPATCH.get(fc.name)
            if fn:
                result = fn(dict(fc.args))
            else:
                result = f"Error: unknown function {fc.name}"
            tool_response_parts.append(
                genai_types.Part.from_function_response(
                    name=fc.name, response={"result": result}
                )
            )

        messages.append(genai_types.Content(role="tool", parts=tool_response_parts))

    if verbose:
        if response.usage_metadata is not None:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
    #print(get_files_info(working_directory="./calculator", directory="."))
