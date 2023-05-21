import re
from functools import reduce

filepath = input("Input file path to import:")
output_filepath = input("Input file path to output:")


def read_file(import_file):
    with open(import_file, encoding="UTF-8", mode="rt") as f:
        read_text_list = f.readlines()

    return read_text_list


def aggregate_attrib_baseclass(text_list):
    current_class = ""  # 現在のクラス名を保持する変数
    class_attributes = []  # クラスの属性値を格納する2次元配列
    for _, line in enumerate(text_list):
        if line.startswith("class "):  # クラス定義の開始行になった場合
            current_class = line.split(" ")[1].split("(")[0].replace("\n", "")
        elif current_class != "":  # 現在のクラス名が設定されている場合
            # 行頭にスペースが4つあり、"クラス変数名:型ヒント=初期値"の形式で書かれた場合
            if line.startswith(" " * 4) and ":" in line and "=" in line:
                class_attributes.append(
                    [current_class, line.replace("\n", "")]
                )  # 現在のクラス名、クラス変数名、型ヒントを配列に格納
            # 関数が定義されている行になった場合、属性取得の対象から外れる
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


def change_camel(text_list):
    for i, line in enumerate(text_list):
        if line.startswith(" " * 4):
            matched_str = re.match(r"^ {4}(.+?):.+?=.*$", line)
            if matched_str:
                var_name = matched_str.group(1)
                words = var_name.split("_")
                words = [w.capitalize() for w in words]
                upper_camel_name = reduce(lambda a, b: a + b, words)
                text_list[i] = line.replace(var_name, upper_camel_name)

        if (
            ": List[" in line
            and "= field(default_factory" in line
            and "List[str]" not in line
            and "List[Any]" not in line
        ):
            text_list[i] = ""

    return text_list


def remove_initial_value(text_list):
    for i, line in enumerate(text_list):
        if line.startswith(" " * 4) and ":" in line and "=" in line:
            attribute_name = line.split(":")[0].strip()  # クラス変数名を取得
            attribute_type = line.split(":")[1].split("=")[0].strip()  # 型ヒントを取得
            line_rm_ini = "    " + attribute_name + ": " + attribute_type + "\n"
        # 関数が定義されている行になった場合、属性取得の対象から外れる
        else:
            line_rm_ini = line
        text_list[i] = line_rm_ini

    return text_list


def save_data_to_file(text_list):
    with open(output_filepath, encoding="UTF-8", mode="w") as f:
        f.write("".join(text_list))


def main():
    text_list_read = read_file(filepath)
    text_list_agg = aggregate_attrib_baseclass(text_list_read)
    text_list_camel = change_camel(text_list_agg)
    text_list_rm = remove_initial_value(text_list_camel)
    save_data_to_file(text_list_rm)


if __name__ == "__main__":
    main()
