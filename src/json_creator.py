from graph_definitions import *
import json

test_output = ["returnType functionName", "paramType1 varName1", "paramType2 varName2"]

def create_json(input_list):
    json_list = []
    param_list = []
    for i in range(1, len(input_list)):
        param_list.append(input_list[i])
    json_dict = {
        "parameters": param_list,
        "functionName": input_list[0].split()[1]
    }
    json_list.append(json_dict)
    return json_list

test_json = create_json(test_output)


def convert_json_to_parameter(input_json):
    function_list = []
    # iterate through json objects
    for x in input_json:
        # iterate through parameters
        param_list = []
        for y in x["parameters"]:
            # create parameter object
            param = Parameter(y.split()[1], y.split()[0], False)
            # add parameter to list
            param_list.append(param)
        # create function object
        function = Function(x["functionName"], param_list)
        # add function to list
        function_list.append(function)
    return function_list

read_json_output = convert_json_to_parameter(test_json)

