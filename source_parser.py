import re

def parse_signature(source_code, max_params=10):
    type_name = "[a-zA-Z0-9\_]+"
    variable_name = "[a-zA-Z0-9\_]+"
    space = "\s+"
    any_space = "[\\n\\r\s]*"
    beginning_characters = "[^a-zA-Z0-9\_]*"
    declaration = f"{type_name}{space}{variable_name}"
    parameter = f"{type_name}{space}{variable_name}"
    non_last_parameter = f"(?:{any_space}({parameter}),{any_space})"
    last_parameter = f"(?:{any_space}({parameter}){any_space})"
    regex_string = f"{beginning_characters}({declaration}){any_space}\\({(non_last_parameter + '?')*(max_params-1)}{last_parameter}?\\){any_space}\\{{.*"
    regex = re.compile(regex_string)
    result_tuples = regex.findall(source_code)
    result_list = list(map(lambda signature_tuple: list(signature_tuple), result_tuples))
    return result_list