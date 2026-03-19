import os
from google.genai import types as genai_types


def write_file(working_directory: str, file_path: str, content: str) -> str:
    absolute_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(absolute_working_dir):
        return f"Error: {abs_file_path} is not in the working directory"

    parent_dir = os.path.dirname(abs_file_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return f"Could not create parent dirs {parent_dir}: {e}"

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
        return f"Successfully wrote to file {file_path} {len(content)} characters"
    except Exception as e:
        return f"Could not write to file {file_path} {len(content)} characters: {e}"


schema_write_file = genai_types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory, creating parent directories as needed.",
    parameters=genai_types.Schema(
        type=genai_types.Type.OBJECT,
        properties={
            "file_path": genai_types.Schema(
                type=genai_types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": genai_types.Schema(
                type=genai_types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
