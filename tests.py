from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def main():
    working_dir = "calculator"

    # get_files_info
    # ----------------
    # root_contents = get_files_info(working_dir)
    # print(root_contents)
    # pkg_contents = get_files_info(working_dir, "pkg")
    # print(pkg_contents)
    # parent_contents = get_files_info(working_dir, "../")
    # print(parent_contents)

    # get_file_content
    # -------------------
    # file_content = get_file_content(working_dir, "lorem.txt")
    # print(file_content)
    # file_content = get_file_content(working_dir, "main.py")
    # print(file_content)
    # file_content = get_file_content(working_dir, "pkg/calculator.py")
    # print(file_content)
    # file_content = get_file_content(working_dir, "pkg/notexist.py")
    # print(file_content)
    # file_content = get_file_content(working_dir, "/bin/cat")
    # print(file_content)

    # write_file
    # -------------------
    # print(write_file(working_dir, "lorem2.txt", "test lorem text"))
    # print(write_file(working_dir, "pkg/lorem3.txt", "test lorem text"))
    # print(write_file(working_dir, "/tmp/lorem3.txt", "test lorem text"))

    # run_python_file
    # -------------------
    # print(run_python_file(working_dir, "main.py"))
    # print(run_python_file(working_dir, "tests.py"))
    # print(run_python_file(working_dir, "../main.py"))
    # print(run_python_file(working_dir, "nonexistent.py"))
    # print(run_python_file(working_dir, "lorem.txt"))
    print(run_python_file(working_dir, "main.py", ["3 + 5"]))


if __name__ == "__main__":
    main()