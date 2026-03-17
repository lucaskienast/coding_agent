import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info


def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    print("API Key: ", api_key)

    print("CLI Arguments: ", sys.argv)

    if len(sys.argv) < 2:
        print("Please provide a prompt.")
        sys.exit(1)

    verbose = False

    if len(sys.argv) == 3 and (sys.argv[2] == "--verbose" or sys.argv[2] == "-v"):
        print("Running in verbose mode.")
        verbose = True

    user_prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=messages
    )

    print(response.text)

    if verbose:
        if response is None or response.usage_metadata is None:
            print("Response has no metadata or is None")
            return

        print(f"Prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
