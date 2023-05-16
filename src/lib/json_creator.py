from lib.graph_definitions import *
import json


def create_json_from_regex(input_list):
    json_list = []
    for x in input_list:
        json_list.append({"functionName": x[0], "parameters": x[1:]})
    # convert json_list to json
    return json.dumps(json_list)


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


def convert_json_to_function(data):
    output = []
    for key, value in data.items():
        output.append({
            "packed_param": key,
            "parameters": value
        })
    return output
