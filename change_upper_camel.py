from functools import reduce
import re


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
