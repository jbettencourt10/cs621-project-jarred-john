import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/lib")
from json_creator import convert_json_to_parameter


class PackerDummy:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            contents = json.loads(f.read())
        self.functions = convert_json_to_parameter(contents)
        self.filename = filename

    def minimize(self):
        print("packer dummy!")
        functions_json_format = []
        for func in self.functions:
            functions_json_format.append(func.toJSON())

        new_file = self.filename.split(".")[0] + "_updated.json"
        packed_name = self.filename.split(".")[0] + "_packed.json"

        with open(new_file, 'w') as output_file:
            output_file.write(json.dumps(functions_json_format))

        with open(packed_name, 'w') as packed_file:
            packed_file.write(json.dumps({}))
