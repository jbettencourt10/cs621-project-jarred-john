import sys
import os
import json

# Include lib folder in path for the purpose of using lib functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/lib")

from graph_definitions import *
from json_creator import convert_json_to_parameter


class AggressiveMinimize:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            contents = json.loads(f.read())
        self.functions = convert_json_to_parameter(contents)
        self.packed_id = 0
        self.packed_params = {}
        self.filename = filename

    # Takes in list of type Function, returns list of type Edge
    # Iterates over every pair of parameters in a function, creating an edge. Existing edges increment the cost
    def build_edges(self):
        edges = {}
        for func in self.functions:
            for i in range(0, len(func.parameters)):
                p1 = func.parameters[i]
                for j in range(i+1, len(func.parameters)):
                    p2 = func.parameters[j]
                    subkey1 = p1.name + p1.type
                    subkey2 = p2.name + p2.type
                    key = (subkey1, subkey2)
                    if subkey1 > subkey2:
                        key = (subkey2, subkey1)
                    if key in edges:
                        edges[key].cost += 1
                    else:
                        edges[key] = Edge(p1, p2, 1)
        return list(edges.values())

    def combine(self):  # Combine parameters that have the heaviest edge, updating the functions
        edges = self.build_edges()  # Generate all edges

        if len(edges) == 0:
            return False  # Minimized
        edges.sort(reverse=True, key=lambda x: x.cost)  # Sort by edge cost, descending
        if edges[0].cost == 1:
            return False  # Minimized

        v1 = edges[0].v1
        v2 = edges[0].v2

        # If both are packed
        if v1.packed and v2.packed:  # Unpack and union the set
            packed_v1 = self.packed_params[v1.name]
            packed_v2 = self.packed_params[v2.name]
            combined = packed_v1.union(packed_v2)
        elif v1.packed:  # v1 is packed - add v2 to the set of v1
            packed_v1 = self.packed_params[v1.name]
            packed_v1.add(v2)
            combined = packed_v1
        elif v2.packed:  # v2 is packed - add v1 to the set of v2
            packed_v2 = self.packed_params[v2.name]
            packed_v2.add(v1)
            combined = packed_v2
        else:  # Neither is packed - create a set consisting of v1 and v2
            combined = {v1, v2}
        pname = "pack" + str(self.packed_id)  # Create a unique name for the pack parameter, based on incrementing ID
        self.packed_id += 1  # Increment ID every time a packing is created
        new_param = Parameter(pname, "", True)  # Create parameter and set packing to true
        self.packed_params[pname] = combined  # Add pack parameter mapping to the set of parameters it has

        # Update function parameters
        for function in self.functions:
            new_params = []
            pack_flag = False
            for param in function.parameters:
                if param.packed:  # If param is a packing, check if they are disjoint
                    packed_set = self.packed_params[param.name]
                    if packed_set.isdisjoint(combined):  # No overlap between packed sets
                        new_params.append(param)
                    else:
                        pack_flag = True
                else:
                    if param not in combined:  # Don't include parameters in packed object
                        new_params.append(param)
                    else:  # If no parameter is in the packed object, don't add the object to the parameter list
                        pack_flag = True
            if pack_flag:
                new_params.append(new_param)
            function.parameters = new_params

        return True
    #Percentage
    def combine2(self):  # Combine parameters that have the heaviest edge, updating the functions
        edges = self.build_edges()  # Generate all edges
        if len(edges) == 0:
            return False  # Minimized
        edgeWeights = dict()
        #Find total edge weight for each node
        for i in range(len(edges)):
            if edges[i].v1 in edgeWeights:
                edgeWeights[edges[i].v1] += edges[i].cost
            else:
                edgeWeights[edges[i].v1] = edges[i].cost
            if edges[i].v2 in edgeWeights:
                edgeWeights[edges[i].v2] += edges[i].cost
            else:
                edgeWeights[edges[i].v2] = edges[i].cost
        maxPercentage = 0
        v1 = None
        v2 = None
        #Find percentage of total edge weight for each parameter each edge is /2
        for x in edges:
            perc = (x.cost / edgeWeights[x.v1] + x.cost / edgeWeights[x.v2]) / 2
            if perc > maxPercentage:
                v1 = x.v1
                v2 = x.v2
                maxPercentage = perc

        #Minimized
        if v1 is None or v2 is None:
            return False
        # Sort by edge cost, descending to check if done
        edges.sort(reverse=True, key=lambda x: x.cost)
        if edges[0].cost == 1:
            return False  # Minimized

        # If both are packed
        if v1.packed and v2.packed:  # Unpack and union the set
            packed_v1 = self.packed_params[v1.name]
            packed_v2 = self.packed_params[v2.name]
            combined = packed_v1.union(packed_v2)
        elif v1.packed:  # v1 is packed - add v2 to the set of v1
            packed_v1 = self.packed_params[v1.name]
            packed_v1.add(v2)
            combined = packed_v1
        elif v2.packed:  # v2 is packed - add v1 to the set of v2
            packed_v2 = self.packed_params[v2.name]
            packed_v2.add(v1)
            combined = packed_v2
        else:  # Neither is packed - create a set consisting of v1 and v2
            combined = {v1, v2}
        pname = "pack" + str(self.packed_id)  # Create a unique name for the pack parameter, based on incrementing ID
        self.packed_id += 1  # Increment ID every time a packing is created
        new_param = Parameter(pname, "", True)  # Create parameter and set packing to true
        self.packed_params[pname] = combined  # Add pack parameter mapping to the set of parameters it has

        # Update function parameters
        for function in self.functions:
            new_params = []
            pack_flag = False
            for param in function.parameters:
                if param.packed:  # If param is a packing, check if they are disjoint
                    packed_set = self.packed_params[param.name]
                    if packed_set.isdisjoint(combined):  # No overlap between packed sets
                        new_params.append(param)
                    else:
                        pack_flag = True
                else:
                    if param not in combined:  # Don't include parameters in packed object
                        new_params.append(param)
                    else:  # If no parameter is in the packed object, don't add the object to the parameter list
                        pack_flag = True
            if pack_flag:
                new_params.append(new_param)
            function.parameters = new_params

        return True

    #Weighted Percentage
    def combine3(self):  # Combine parameters that have the heaviest edge, updating the functions
        edges = self.build_edges()  # Generate all edges

        if len(edges) == 0:
            return False  # Minimized
        edgeWeights = dict()
        #Find total edge weight for each node
        for i in range(len(edges)):
            if edges[i].v1 in edgeWeights:
                edgeWeights[edges[i].v1] += edges[i].cost
            else:
                edgeWeights[edges[i].v1] = edges[i].cost
            if edges[i].v2 in edgeWeights:
                edgeWeights[edges[i].v2] += edges[i].cost
            else:
                edgeWeights[edges[i].v2] = edges[i].cost
        maxPercentage = 0
        v1 = None
        v2 = None
        #Find percentage of total edge weight for each parameter each edge is and multiply by edge weight
        for x in edges:
            perc = (x.cost * (x.cost / edgeWeights[x.v1]) + x.cost * (x.cost / edgeWeights[x.v2]))
            if perc > maxPercentage:
                v1 = x.v1
                v2 = x.v2
                maxPercentage = perc
        #Minimized
        if v1 is None or v2 is None:
            return False
        # Sort by edge cost, descending to check if done
        edges.sort(reverse=True, key=lambda x: x.cost)
        if edges[0].cost == 1:
            return False  # Minimized

        # If both are packed
        if v1.packed and v2.packed:  # Unpack and union the set
            packed_v1 = self.packed_params[v1.name]
            packed_v2 = self.packed_params[v2.name]
            combined = packed_v1.union(packed_v2)
        elif v1.packed:  # v1 is packed - add v2 to the set of v1
            packed_v1 = self.packed_params[v1.name]
            packed_v1.add(v2)
            combined = packed_v1
        elif v2.packed:  # v2 is packed - add v1 to the set of v2
            packed_v2 = self.packed_params[v2.name]
            packed_v2.add(v1)
            combined = packed_v2
        else:  # Neither is packed - create a set consisting of v1 and v2
            combined = {v1, v2}
        pname = "pack" + str(self.packed_id)  # Create a unique name for the pack parameter, based on incrementing ID
        self.packed_id += 1  # Increment ID every time a packing is created
        new_param = Parameter(pname, "", True)  # Create parameter and set packing to true
        self.packed_params[pname] = combined  # Add pack parameter mapping to the set of parameters it has

        # Update function parameters
        for function in self.functions:
            new_params = []
            pack_flag = False
            for param in function.parameters:
                if param.packed:  # If param is a packing, check if they are disjoint
                    packed_set = self.packed_params[param.name]
                    if packed_set.isdisjoint(combined):  # No overlap between packed sets
                        new_params.append(param)
                    else:
                        pack_flag = True
                else:
                    if param not in combined:  # Don't include parameters in packed object
                        new_params.append(param)
                    else:  # If no parameter is in the packed object, don't add the object to the parameter list
                        pack_flag = True
            if pack_flag:
                new_params.append(new_param)
            function.parameters = new_params

        return True

    # Minimizes functions
    def minimize(self):
        while self.combine():
            pass

        functions_json_format = []
        for func in self.functions:
            functions_json_format.append(func.toJSON())

        new_file = self.filename.split(".")[0] + "_updated.json"
        packed_name = self.filename.split(".")[0]+"_packed.json"

        with open(new_file, 'w') as output_file:
            output_file.write(json.dumps(functions_json_format))

        packed_json_data = []

        for k, v in self.packed_params.items():
            packed_json_data.append({"packed_param": k,  "parameters": [p.toJSON() for p in list(v)]})

        with open(packed_name, 'w') as packed_file:
            packed_file.write(json.dumps(packed_json_data))


if __name__ == "__main__":
    aggressive_minimize = AggressiveMinimize("test.json")
    aggressive_minimize.minimize()
    minimized_functions = aggressive_minimize.functions
    packed_params = aggressive_minimize.packed_params
    for mfunc in minimized_functions:
        debug_print_function(mfunc)
    debug_print_packed_params(packed_params)
