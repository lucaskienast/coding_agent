from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info


def main():
    working_dir = "calculator"

    # get_files_info
    root_contents = get_files_info(working_dir)
    print(root_contents)
    pkg_contents = get_files_info(working_dir, "pkg")
    print(pkg_contents)
    parent_contents = get_files_info(working_dir, "../")
    print(parent_contents)

    # get_file_content
    # file_content = get_file_content(working_dir, "lorem.txt")
    # print(file_content)
    file_content = get_file_content(working_dir, "main.py")
    print(file_content)
    file_content = get_file_content(working_dir, "pkg/calculator.py")
    print(file_content)
    file_content = get_file_content(working_dir, "pkg/notexist.py")
    print(file_content)
    file_content = get_file_content(working_dir, "/bin/cat")
    print(file_content)

if __name__ == "__main__":
    main()