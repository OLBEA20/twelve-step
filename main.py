import argparse
from os import walk

from jivago_streams import Stream

from typing import List, Tuple

def write_dependency_file(dependencies: Tuple[str, List[str]]):
    file = open("dependency.dot", "a+")
    Stream(dependencies[1]).forEach(lambda dependency: file.write(f"{dependencies[0]} -> {dependency}\n"))
    file.close()


def find_classes(file_to_imported_classes: Tuple[str, List[str]]) -> List[Tuple[str, List[str]]]:
    classes = []
    with open(file_to_imported_classes[0]) as file:
        line = file.readline()
        while line:
            if line.startswith("class"):
                end_of_class_name_index = line.find("(") if line.find("(") != -1 else line.find(":")
                start_of_class_name_index = len("class ")
                classes.append(line[start_of_class_name_index:end_of_class_name_index])
            line = file.readline()
    
    return Stream(classes).map(lambda clasz: (clasz, file_to_imported_classes[1])).toList()



def find_imported_classes(file_to_imports: Tuple[str, List[str]]) -> Tuple[str, List[str]]:
    classes = []
    for imp in file_to_imports[1]:
        import_location = imp.index(" import ") + len(" import ")
        class_imported = imp[import_location:]
        classes += class_imported.replace(" ", "").split(',')
    return (file_to_imports[0], classes)


def contract_line(file, line: str) -> str:
    line = line.replace("(", "")
    new_line = file.readline()
    while ")" not in new_line:
        line += new_line
        new_line = file.readline()
    line = line.replace("\n", "")
    return line


def find_imports(file_path: str) -> List[str]:
    imports = []
    with open(file_path) as file:
        line = file.readline()
        while line:
            if line.startswith("from ") and "typing" not in line:
                if "(" in line:
                    imports.append(contract_line(file, line))
                else:
                    imports.append(line[:-1])
            line = file.readline()

    return imports


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_path")
    args = parser.parse_args()

    file = open("dependency.dot", "a+")
    file.write("digraph dependency_graph {\n")
    file.close()

    for (path, directories, files) in walk(args.project_path):
        Stream(files) \
            .filter(lambda file: file.endswith(".py")) \
            .map(lambda file: f"{path}/{file}") \
            .map(lambda file_path: (file_path, find_imports(file_path))) \
            .map(find_imported_classes) \
            .map(find_classes) \
            .flat() \
            .forEach(write_dependency_file)

    file = open("dependency.dot", "a+")
    file.write("}\n")
    file.close()

        