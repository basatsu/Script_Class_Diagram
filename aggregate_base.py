import re


def aggregate_attrib_baseclass(text_list: list[str]):
    current_class = ""
    class_attributes = []
    for _, line in enumerate(text_list):
        if line.startswith("class "):
            current_class = line.split(" ")[1].split("(")[0].replace("\n", "")
        elif current_class != "":
            if line.startswith(" " * 4) and ":" in line and "=" in line:
                class_attributes.append([current_class, line.replace("\n", "")])
            elif line.startswith("def "):
                continue

    for i, line in enumerate(text_list):
        if re.match(r"class\s+(\w+)\(([\w\s,]+)\):", line):
            match = re.match(r"class\s+(\w+)\(([\w\s,]+)\):", line)
            base_classes = [base.strip() for base in match.group(2).split(",")]
            for base_class in base_classes:
                if base_class.endswith(("Base", "Mixin")):
                    for attr in class_attributes:
                        cut_attr = attr[0].strip().replace(":", "")
                        if base_class.strip() == cut_attr:
                            if i + 1 < len(text_list):
                                text_list.insert(i + 1, f"{attr[1]}\n")

    return text_list
