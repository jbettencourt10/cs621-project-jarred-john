packed_id = 0


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


class Function:
    def __init__(self, name, params):
        self.name = name
        self.parameters = params


# Takes in list of type Function, returns list of type Edge
def build_edges(functions):
    edges = {}
    for func in functions:
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


# Combine parameters that have the heaviest edge, updating the functions
def combine(functions, packed_params):
    global packed_id

    edges = build_edges(functions)  # Generate all edges

    if len(edges) == 0:
        return None, None  # Minimized
    edges.sort(reverse=True, key=lambda x: x.cost)  # Sort by edge cost, descending
    if edges[0].cost == 1:
        return None, None  # Minimized

    v1 = edges[0].v1
    v2 = edges[0].v2

    # If both are packed
    if v1.packed and v2.packed:
        packed_v1 = packed_params[v1.name]
        packed_v2 = packed_params[v2.name]
        combined = packed_v1.union(packed_v2)
    elif v1.packed:  # v1 is packed
        packed_v1 = packed_params[v1.name]
        packed_v1.add(v2)
        combined = packed_v1
    elif v2.packed:  # v2 is packed
        packed_v2 = packed_params[v2.name]
        packed_v2.add(v1)
        combined = packed_v2
    else:  # Neither is packed
        combined = {v1, v2}
    pname = "pack" + str(packed_id)
    packed_id += 1
    new_param = Parameter(pname, "", True)
    packed_params[pname] = combined

    # Update function parameters
    for function in functions:
        new_params = []
        pack_flag = False
        for param in function.parameters:
            if param.packed:  # If param is a packing, check if they are disjoint
                packed_set = packed_params[param.name]
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

    return functions, packed_params


# Minimizes functions
def minimize(functions):
    packed_params = {}
    while True:
        new_functions, new_packed_params = combine(functions, packed_params)
        if new_functions is None:  # Done
            break
        functions = new_functions
        packed_params = new_packed_params
    return functions, packed_params


def test_func():
    p1 = Parameter("foo", "int")
    p2 = Parameter("bar", "str")
    p3 = Parameter("baz", "int")
    p4 = Parameter("bop", "int")
    f1 = Function("foobar", [p1, p2])
    f2 = Function("foobazbop", [p1, p3, p4])
    f3 = Function("foobaz", [p1, p3])
    functions, packed_params = minimize([f1, f2, f3])
    for f in functions:
        print_function(f)
    print_packed_params(packed_params)


def print_packed_params(packed_params):
    print("Packed Parameters:")
    for name, params in packed_params.items():
        print("Name: %s" % name)
        for p in list(params):
            print_parameter(p)
        print()


def print_function(function):
    print("Name: %s" % function.name)
    for param in function.parameters:
        print_parameter(param)
    print()


def print_edges(edges):
    for edge in edges:
        print("Vertex 1: " + edge.v1.name + ":" + edge.v1.type)
        print("Vertex 2: " + edge.v2.name + ":" + edge.v2.type)
        print("Cost: " + str(edge.cost)+"\n")


def print_parameter(p):
    print("Parameter %s:%s" % (p.name, p.type))


if __name__ == "__main__":
    test_func()
