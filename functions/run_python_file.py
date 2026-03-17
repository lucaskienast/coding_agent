import os
import subprocess
from typing import Iterable


def run_python_file(working_directory: str, file_path: str, args: Iterable[str] | None = None) -> str:
    absolute_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(absolute_working_dir):
        return f"Error: {abs_file_path} is not in the working directory"
    if not os.path.isfile(abs_file_path):
        return f"Error: {abs_file_path} is not a file"
    if not file_path.endswith(".py"):
        return f"Error: {file_path} is not a .py file"

    try:
        final_args = ["python3", abs_file_path]
        final_args.extend(args)
        result = subprocess.run(
            final_args,
            cwd=absolute_working_dir,
            capture_output=True,
            timeout=30,
        )

        if result.stdout == "" and result.stderr == "":
            return "No output produced."

        output = f"""
        STDOUT: {result.stdout}
        STDERR: {result.stderr}
        """

        if result.returncode != 0:
            output += f"Process exited with return code {result.returncode}"

        return output
    except Exception as e:
        return f"Error executing Python file {abs_file_path}: {e}"