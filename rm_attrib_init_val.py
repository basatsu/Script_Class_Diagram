def remove_initial_value(text_list):
    for i, line in enumerate(text_list):
        if line.startswith(" " * 4) and ":" in line and "=" in line:
            attribute_name = line.split(":")[0].strip()
            attribute_type = line.split(":")[1].split("=")[0].strip()
            line_rm_ini = "    " + attribute_name + ": " + attribute_type + "\n"
        else:
            line_rm_ini = line
        text_list[i] = line_rm_ini

    return text_list
