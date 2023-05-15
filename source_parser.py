import regex
from pathlib import Path

def parse_signature(source_code, max_params=10):
    space = "\s+"
    any_space = "[\\n\\r\s]*"
    type_name = f"(?:[a-zA-Z0-9\_:]+(?:<(?:{any_space}[a-zA-Z0-9\_:]+,?)+>)?)"
    variable_name = "[a-zA-Z0-9\_:]+"
    beginning_characters = "[^a-zA-Z0-9\_]*"
    declaration = f"{type_name}{any_space}[&\*]*{space}[&\*]*{variable_name}"
    parameter = lambda capture: f"(?:{any_space}(?:const{space})?{('(' if capture else '') + declaration + (')' if capture else '')},?{any_space})"
    regex_string = f"{beginning_characters}(?:const{space})?({declaration}){any_space}\\({(parameter(True) + '?')*(max_params)}{parameter(False)}*\\){any_space}(?:const{any_space})?\\{{.*"
    expression = regex.compile(regex_string)
    result_tuples = expression.findall(source_code)
    result_list = list(map(lambda signature_tuple: list(signature_tuple), result_tuples))
    return result_list