import regex
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+"/lib")

import json_creator


def parse_signature(source_code, max_params=10):
    space = "\s+"
    any_space = "[\\n\\r\s]*"
    type_name = f"(?:[a-zA-Z0-9\_][a-zA-Z0-9\_:]*(?:<(?:{any_space}[a-zA-Z0-9\_:]+,?)+>)?)"
    variable_name = "[a-zA-Z0-9\_][a-zA-Z0-9\_:]*"
    beginning_characters = "[^a-zA-Z0-9\_]*"
    declaration = f"{type_name}{any_space}[&\*]*{space}[&\*]*{variable_name}"
    parameter = lambda \
        capture: f"(?:{any_space}(?:const{space})?{('(' if capture else '') + declaration + (')' if capture else '')},?{any_space})"
    regex_string = f"{beginning_characters}(?:const{space})?({declaration}){any_space}\\({(parameter(True) + '?') * (max_params)}{parameter(False)}*\\){any_space}(?:const{any_space})?\\{{.*"
    expression = regex.compile(regex_string)
    result_tuples = expression.findall(source_code)
    result_list = list(
        map(lambda signature_tuple: [regex.sub(" +", " ", x) for x in signature_tuple if x], result_tuples))
    return result_list


class SourceParser:

    def __init__(self, filename, max_params):
        self.max_params = max_params
        self.filename = filename

    def parse(self):
        with open(self.filename, 'r') as f:
            contents = f.read()
        result_list = parse_signature(contents, self.max_params)
        json_filename = self.filename.split(".")[0]
        with open(json_filename+".json", 'w') as json_file:
            json_file.write(json_creator.create_json_from_regex(result_list))


if __name__ == "__main__":
    sp = SourceParser('test.c', 6)
    # print(sp.parse_signature(Path("test_data/VBORenderer.cc.nocomments").read_text(), 6))
    sp.parse()
