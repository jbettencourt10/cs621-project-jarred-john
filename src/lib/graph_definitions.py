# Class Definitions
class Edge:
    def __init__(self, v1, v2, c):
        self.v1 = v1
        self.v2 = v2
        self.cost = c


class Parameter:
    def __init__(self, name, ptype, packed=False):
        self.name = name
        self.type = ptype
        self.packed = packed

    def __hash__(self):
        return hash((self.name, self.type, self.packed))

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name and self.type == other.type and self.packed == other.packed

    def toJSON(self):
        if self.type == "":
            return self.name
        return self.type + " " + self.name


class Function:
    def __init__(self, name, params):
        self.name = name
        self.parameters = params

    def toJSON(self):
        return {"functionName": self.name, "parameters": [p.toJSON() for p in self.parameters]}


# FUNCTIONS
def debug_print_packed_params(packed_params):
    print("Packed Parameters:")
    for name, params in packed_params.items():
        print("Name: %s" % name)
        for p in list(params):
            debug_print_parameter(p)
        print()


def debug_print_function(function):
    print("Name: %s" % function.name)
    for param in function.parameters:
        debug_print_parameter(param)
    print()


def debug_print_edges(edges):
    for edge in edges:
        print("Vertex 1: " + edge.v1.name + ":" + edge.v1.type)
        print("Vertex 2: " + edge.v2.name + ":" + edge.v2.type)
        print("Cost: " + str(edge.cost)+"\n")


def debug_print_parameter(p):
    print("Parameter %s:%s" % (p.name, p.type))
