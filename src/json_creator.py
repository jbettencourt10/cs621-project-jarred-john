from graph_definitions import *
import json

test_output = [['void VBORenderer::resize', 'int w', 'int h'], ['bool VBORenderer::getShaderColor', 'Renderer::ColorMode colormode', 'Color4f& color', 'Color4f& outcolor'], ['size_t VBORenderer::getSurfaceBufferSize', 'std::shared_ptr<CSGProducts>& products', 'bool highlight_mode', 'bool background_mode', 'bool unique_geometry'], ['size_t VBORenderer::getSurfaceBufferSize', 'CSGChainObject& csgobj', 'bool highlight_mode', 'bool background_mode', 'OpenSCADOperator type', 'bool unique_geometry'], ['size_t VBORenderer::getSurfaceBufferSize', 'PolySet& polyset', 'csgmode_e csgmode'], ['size_t VBORenderer::getEdgeBufferSize', 'std::shared_ptr<CSGProducts>& products', 'bool highlight_mode', 'bool background_mode', 'bool unique_geometry'], ['size_t VBORenderer::getEdgeBufferSize', 'CSGChainObject& csgobj', 'bool highlight_mode', 'bool background_mode', 'OpenSCADOperator type', 'bool unique_geometry'], ['size_t VBORenderer::getEdgeBufferSize', 'PolySet& polyset', 'csgmode_e csgmode'], ['void VBORenderer::create_vertex', 'VertexArray& vertex_array', 'Color4f& color', 'std::array<Vector3d, 3>& points', 'std::array<Vector3d, 3>& normals', 'size_t active_point_index', 'size_t primitive_index'], ['void VBORenderer::create_triangle', 'VertexArray& vertex_array', 'Color4f& color', 'Vector3d& p0', 'Vector3d& p1', 'Vector3d& p2', 'size_t primitive_index'], ['Vector3d uniqueMultiply', 'std::unordered_map<Vector3d, size_t>& vert_mult_map', 'std::vector<Vector3d>& mult_verts', 'Vector3d& in_vert', 'Transform3d& m'], ['void VBORenderer::create_surface', 'PolySet& ps', 'VertexArray& vertex_array', 'csgmode_e csgmode', 'Transform3d& m', 'Color4f& color'], ['void VBORenderer::create_edges', 'PolySet& ps', 'VertexArray& vertex_array', 'csgmode_e csgmode', 'Transform3d& m', 'Color4f& color'], ['void VBORenderer::create_polygons', 'PolySet& ps', 'VertexArray& vertex_array', 'csgmode_e csgmode', 'Transform3d& m', 'Color4f& color'], ['void VBORenderer::add_shader_data', 'VertexArray& vertex_array'], ['void VBORenderer::add_shader_pointers', 'VertexArray& vertex_array'], ['void VBORenderer::shader_attribs_enable'], ['void VBORenderer::shader_attribs_disable']]

def create_json_from_regex(input_list):
    json_list = []
    for x in input_list:
        json_list.append({"functionName": x[0], "parameters": x[1:]})
    return json_list

test_json = create_json_from_regex(test_output)

print(test_json)

def convert_json_to_nodes(input_json):
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

read_json_output = convert_json_to_nodes(test_json)
