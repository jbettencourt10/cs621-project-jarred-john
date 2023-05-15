from unittest import TestCase
import source_parser

class BasicParamsCase(TestCase):
    def test_no_params(self):
        self.assertListEqual([["int myFunc"]], source_parser.parse_signature("int myFunc() {", 3))
    def test_simple_params(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc(bool myVarA, String myVarB) {", 2))
    def test_too_many_params(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc(bool myVarA, String myVarB, float myVarC) {", 2))
    def test_not_enough_params(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB", "float myVarC"]], source_parser.parse_signature("int myFunc(bool myVarA, String myVarB, float myVarC) {", 6))
    def test_no_spacing(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc(bool myVarA,String myVarB){", 2))
    def test_everywhere_spacing(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("  int myFunc (  bool myVarA,  String myVarB  ) {  ", 2))
    def test_newlines(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc \n  (\n bool myVarA,\n  String myVarB\n)\n{\n", 2))

class MultiLineCase(TestCase):
    def test_two_functions(self):
        self.assertListEqual([["int myFunc1", "bool myVarA", "String myVarB", "float myVarC"], ["arr myFunc2", "double otherVarA", "bool otherVarB"]], source_parser.parse_signature("int myFunc1(bool myVarA, String myVarB, float myVarC) {\nx++;\n}\n    arr myFunc2( double otherVarA, bool otherVarB)\n{\n}", 6))
    def test_comment_in_between(self):
        self.assertListEqual([["int myFunc1", "bool myVarA", "String myVarB", "float myVarC"], ["arr myFunc2", "double otherVarA", "bool otherVarB"]], source_parser.parse_signature("int myFunc1(bool myVarA, String myVarB, float myVarC) {\nx++;\n}\n  //there's just a comment here\n  arr myFunc2( double otherVarA, bool otherVarB)\n{\n}", 6))
    def test_function_call_in_body(self):
        self.assertListEqual([["int myFunc1", "bool myVarA", "String myVarB", "float myVarC"], ["arr myFunc2", "double otherVarA", "bool otherVarB"]], source_parser.parse_signature("int myFunc1(bool myVarA, String myVarB, float myVarC) {\n    otherFunctionCall(x, y, zVariable, 1);\n}\n  arr myFunc2( double otherVarA, bool otherVarB)\n{\n}", 6))
class OpenScadCase(TestCase):
    def test_const_and_complex_declr(self):
        self.assertListEqual([["size_t VBORenderer::getSurfaceBufferSize", "std::shared_ptr<CSGProducts>& products", "bool highlight_mode", "bool background_mode", "bool unique_geometry"]], source_parser.parse_signature("size_t VBORenderer::getSurfaceBufferSize(const std::shared_ptr<CSGProducts>& products, bool highlight_mode, bool background_mode, bool unique_geometry) const\n{\n  size_t buffer_size = 0;", 4))
    def test_multiple_template_params(self):
        self.assertListEqual([['void VBORenderer::create_vertex', 'VertexArray& vertex_array', 'Color4f& color', 'std::array<Vector3d, 3>& points', 'std::array<Vector3d, 3>& normals', 'size_t active_point_index', 'size_t primitive_index']], source_parser.parse_signature("void VBORenderer::create_vertex(VertexArray& vertex_array, const Color4f& color,\n                                const std::array<Vector3d, 3>& points,\n                                const std::array<Vector3d, 3>& normals,\n                                size_t active_point_index, size_t primitive_index,\n                                double z_offset, size_t shape_size,\n                                size_t shape_dimensions, bool outlines,\n                                bool mirror) const\n{", 6))
# TODO array types
# TODO there should be tests for public and static modifiers to function declarations.