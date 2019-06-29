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


def remove_new_line_character(file_to_imports: Tuple[str, List[str]]) -> Tuple[str, List[str]]:
    lines_without_new_line_characters = []
    for line in file_to_imports[1]:
        lines_without_new_line_characters.append(line.replace("\n", ""))

    return (file_to_imports[0], lines_without_new_line_characters)
