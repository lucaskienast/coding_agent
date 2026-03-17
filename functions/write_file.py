import os


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
