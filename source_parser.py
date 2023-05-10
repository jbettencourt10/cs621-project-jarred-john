import re

def parse_signature(source_code):
    type_name = "[a-zA-Z0-9\_]+"
    variable_name = "[a-zA-Z0-9\_]+"
    space = "\s+"
    any_space = "[\\n\\r\s]*"
    beginning_characters = "[^a-zA-Z0-9\_]*"
    regex_string = f"{beginning_characters}({type_name}{space}{variable_name}){any_space}\\((?:({any_space}{type_name}{space}{variable_name}){any_space},{any_space})*{any_space}({type_name}{space}{variable_name})?\\){any_space}\\{{.*"
    regex = re.compile(regex_string)
    result_tuples = regex.findall(source_code)
    result_list = list(map(lambda signature_tuple: list(signature_tuple), result_tuples))
    return result_list