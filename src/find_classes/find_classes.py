from typing import List, Tuple

CLASS_KEYWORD = "class "


def find_classes(
    file_to_imported_classes: Tuple[str, List[str]]
) -> List[Tuple[str, List[str]]]:
    with open(file_to_imported_classes[0]) as file:
        lines = file.readlines()
        classes = _find_classes_in(lines)
    return [(clazz, file_to_imported_classes[1]) for clazz in classes]


def _find_classes_in(lines: List[str]):
    return [
        _find_class_name_in(line) for line in lines if line.startswith(CLASS_KEYWORD)
    ]


def _find_class_name_in(line: str) -> str:
    end_of_class_name_index = line.find("(") if line.find("(") != -1 else line.find(":")
    start_of_class_name_index = len(CLASS_KEYWORD)
    return line[start_of_class_name_index:end_of_class_name_index]
