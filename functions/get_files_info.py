import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    absolute_working_dir = os.path.abspath(working_directory)
    #print("absolute_working_dir", absolute_working_dir)
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    #print("abs_dir", abs_dir)

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
