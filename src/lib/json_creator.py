from lib.graph_definitions import *
import json

test__regex_output = [["void VBORenderer::resize", "int w", "int h"], ["bool VBORenderer::getShaderColor", "Renderer::ColorMode colormode", "Color4f& color", "Color4f& outcolor"], ["size_t VBORenderer::getSurfaceBufferSize", "std::shared_ptr<CSGProducts>& products", "bool highlight_mode", "bool background_mode", "bool unique_geometry"], ["size_t VBORenderer::getSurfaceBufferSize", "CSGChainObject& csgobj", "bool highlight_mode", "bool background_mode", "OpenSCADOperator type", "bool unique_geometry"], ["size_t VBORenderer::getSurfaceBufferSize", "PolySet& polyset", "csgmode_e csgmode"], ["size_t VBORenderer::getEdgeBufferSize", "std::shared_ptr<CSGProducts>& products", "bool highlight_mode", "bool background_mode", "bool unique_geometry"], ["size_t VBORenderer::getEdgeBufferSize", "CSGChainObject& csgobj", "bool highlight_mode", "bool background_mode", "OpenSCADOperator type", "bool unique_geometry"], ["size_t VBORenderer::getEdgeBufferSize", "PolySet& polyset", "csgmode_e csgmode"], ["void VBORenderer::create_vertex", "VertexArray& vertex_array", "Color4f& color", "std::array<Vector3d, 3>& points", "std::array<Vector3d, 3>& normals", "size_t active_point_index", "size_t primitive_index"], ["void VBORenderer::create_triangle", "VertexArray& vertex_array", "Color4f& color", "Vector3d& p0", "Vector3d& p1", "Vector3d& p2", "size_t primitive_index"], ["Vector3d uniqueMultiply", "std::unordered_map<Vector3d, size_t>& vert_mult_map", "std::vector<Vector3d>& mult_verts", "Vector3d& in_vert", "Transform3d& m"], ["void VBORenderer::create_surface", "PolySet& ps", "VertexArray& vertex_array", "csgmode_e csgmode", "Transform3d& m", "Color4f& color"], ["void VBORenderer::create_edges", "PolySet& ps", "VertexArray& vertex_array", "csgmode_e csgmode", "Transform3d& m", "Color4f& color"], ["void VBORenderer::create_polygons", "PolySet& ps", "VertexArray& vertex_array", "csgmode_e csgmode", "Transform3d& m", "Color4f& color"], ["void VBORenderer::add_shader_data", "VertexArray& vertex_array"], ["void VBORenderer::add_shader_pointers", "VertexArray& vertex_array"], ["void VBORenderer::shader_attribs_enable"], ["void VBORenderer::shader_attribs_disable"]]

def create_json_from_regex(input_list):
    json_list = []
    for x in input_list:
        json_list.append({"functionName": x[0], "parameters": x[1:]})
    # convert json_list to json
    return json.dumps(json_list)

test_json = create_json_from_regex(test__regex_output)

def convert_json_to_parameter(input_json):
    input_json = json.loads(input_json)
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

test_json = [{"functionName": "void VBORenderer::resize", "parameters": ["int w", "int h"]}, {"functionName": "bool VBORenderer::getShaderColor", "parameters": ["Renderer::ColorMode colormode", "Color4f& color", "Color4f& outcolor"]}, {"functionName": "size_t VBORenderer::getSurfaceBufferSize", "parameters": ["std::shared_ptr<CSGProducts>& products", "bool highlight_mode", "bool background_mode", "bool unique_geometry"]}, {"functionName": "size_t VBORenderer::getSurfaceBufferSize", "parameters": ["CSGChainObject& csgobj", "bool highlight_mode", "bool background_mode", "OpenSCADOperator type", "bool unique_geometry"]}, {"functionName": "size_t VBORenderer::getSurfaceBufferSize", "parameters": ["PolySet& polyset", "csgmode_e csgmode"]}, {"functionName": "size_t VBORenderer::getEdgeBufferSize", "parameters": ["std::shared_ptr<CSGProducts>& products", "bool highlight_mode", "bool background_mode", "bool unique_geometry"]}, {"functionName": "size_t VBORenderer::getEdgeBufferSize", "parameters": ["CSGChainObject& csgobj", "bool highlight_mode", "bool background_mode", "OpenSCADOperator type", "bool unique_geometry"]}, {"functionName": "size_t VBORenderer::getEdgeBufferSize", "parameters": ["PolySet& polyset", "csgmode_e csgmode"]}, {"functionName": "void VBORenderer::create_vertex", "parameters": ["VertexArray& vertex_array", "Color4f& color", "std::array<Vector3d, 3>& points", "std::array<Vector3d, 3>& normals", "size_t active_point_index", "size_t primitive_index"]}, {"functionName": "void VBORenderer::create_triangle", "parameters": ["VertexArray& vertex_array", "Color4f& color", "Vector3d& p0", "Vector3d& p1", "Vector3d& p2", "size_t primitive_index"]}, {"functionName": "Vector3d uniqueMultiply", "parameters": ["std::unordered_map<Vector3d, size_t>& vert_mult_map", "std::vector<Vector3d>& mult_verts", "Vector3d& in_vert", "Transform3d& m"]}, {"functionName": "void VBORenderer::create_surface", "parameters": ["PolySet& ps", "VertexArray& vertex_array", "csgmode_e csgmode", "Transform3d& m", "Color4f& color"]}, {"functionName": "void VBORenderer::create_edges", "parameters": ["PolySet& ps", "VertexArray& vertex_array", "csgmode_e csgmode", "Transform3d& m", "Color4f& color"]}, {"functionName": "void VBORenderer::create_polygons", "parameters": ["PolySet& ps", "VertexArray& vertex_array", "csgmode_e csgmode", "Transform3d& m", "Color4f& color"]}, {"functionName": "void VBORenderer::add_shader_data", "parameters": ["VertexArray& vertex_array"]}, {"functionName": "void VBORenderer::add_shader_pointers", "parameters": ["VertexArray& vertex_array"]}, {"functionName": "void VBORenderer::shader_attribs_enable", "parameters": []}, {"functionName": "void VBORenderer::shader_attribs_disable", "parameters": []}]

def convert_json_to_function(input_json):
    input_json = json.loads(input_json)
    for x in input_json:
        # create function object
        function = Function(x["functionName"], param_list)
        # add function to list
        function_list.append(function)

test_function_json_output = [{
    "packed_param": "pack0",
    "parameters": ["int baz", "int bar", "int foo"]
},
    {
    "packed_param": "pack1",
    "parameters": ["int baz", "int bar", "int foo"]
    }
]

print(convert_json_to_function(test_function_json))
