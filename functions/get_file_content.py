import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    absolute_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(absolute_working_dir):
        return f"Error: {abs_file_path} is not in the working directory"
    if not os.path.isfile(abs_file_path):
        return f"Error: {abs_file_path} is not a file"

    file_content = ""

    try:
        with open(abs_file_path, "r") as file:
            file_content = file.read(MAX_CHARS)
            if len(file_content) >= MAX_CHARS:
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS}]'
    except Exception as e:
        print(e)
        return file_content

    return file_content
