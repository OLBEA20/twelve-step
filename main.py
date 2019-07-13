import argparse
from os import walk

from jivago_streams import Stream

from src.dependency_graph import remove_new_line_character, write_dependency_file
from src.find_classes.find_classes import find_classes
from src.find_imports.find_imports_in_file import find_imports_in_file
from src.find_imported_classes.find_imported_classes import find_imported_classes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path")
    args = parser.parse_args()

    file = open("dependency.dot", "a+")
    file.write("digraph dependency_graph {\n")
    file.close()

    for (path, directories, files) in walk(args.project_path):
        Stream(files).filter(lambda file: file.endswith(".py")).map(
            lambda file: f"{path}/{file}"
        ).map(lambda file_path: (file_path, find_imports_in_file(file_path))).map(
            find_imported_classes
        ).map(
            remove_new_line_character
        ).map(
            find_classes
        ).flat().forEach(
            write_dependency_file
        )

    file = open("dependency.dot", "a+")
    file.write("}\n")
    file.close()
