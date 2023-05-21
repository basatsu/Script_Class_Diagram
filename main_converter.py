import aggregate_base
import change_upper_camel
import rm_attrib_init_val

filepath = input("Input file path to import:")
output_filepath = input("Input file path to output:")


def read_file(import_file):
    with open(import_file, encoding="UTF-8", mode="rt") as f:
        read_text_list = f.readlines()

    return read_text_list


def save_data_to_file(text_list):
    with open(output_filepath, encoding="UTF-8", mode="w") as f:
        f.write("".join(text_list))


def main():
    text_list_read = read_file(filepath)
    text_list_agg = aggregate_base.aggregate_attrib_baseclass(text_list_read)
    text_list_camel = change_upper_camel.change_camel(text_list_agg)
    text_list_rm = rm_attrib_init_val.remove_initial_value(text_list_camel)
    save_data_to_file(text_list_rm)


if __name__ == "__main__":
    main()
