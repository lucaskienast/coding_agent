import os
from google.genai import types as genai_types


def get_files_info(working_directory: str, directory: str = ".") -> str:
    absolute_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not abs_dir.startswith(absolute_working_dir):
        return f"Error: {abs_dir} is not in the working directory"

    dir_contents = os.listdir(abs_dir)

    final_response = ""

    for dir_content in dir_contents:
        dir_content_path = os.path.join(abs_dir, dir_content)
        is_dir = os.path.isdir(dir_content_path)
        size = os.path.getsize(dir_content_path)
        final_response += f"- {dir_content}: is_dir={is_dir}, file_size={size} bytes\n"

    return final_response


schema_get_files_info = genai_types.FunctionDeclaration(
    name="get_files_info",
    description="Lists the contents of a directory within the working directory, returning each entry's name, type (file or directory), and size in bytes.",
    parameters=genai_types.Schema(
        type=genai_types.Type.OBJECT,
        properties={
            "directory": genai_types.Schema(
                type=genai_types.Type.STRING,
                description="The directory to list, relative to the working directory. Defaults to '.' (the working directory itself).",
            ),
        },
        required=[],
    ),
)
