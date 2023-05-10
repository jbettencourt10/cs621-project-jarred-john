from unittest import TestCase
import source_parser

class BasicParamsCase(TestCase):
    def test_no_params(self):
        self.assertListEqual([["int myFunc", "", "", ""]], source_parser.parse_signature("int myFunc() {", 3))
    def test_simple_params(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc(bool myVarA, String myVarB) {", 2))
    def test_too_many_params(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc(bool myVarA, String myVarB, float myVarC) {", 2))
    def test_not_enough_params(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB", "float myVarC", "", "", ""]], source_parser.parse_signature("int myFunc(bool myVarA, String myVarB, float myVarC) {", 6))
    def test_no_spacing(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc(bool myVarA,String myVarB){", 2))
    def test_everywhere_spacing(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("  int myFunc (  bool myVarA,  String myVarB  ) {  ", 2))
    def test_newlines(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc \n  (\n bool myVarA,\n  String myVarB\n)\n{\n", 2))

class MultiLineCase(TestCase):
    def test_two_functions(self):
        self.assertListEqual([["int myFunc1", "bool myVarA", "String myVarB", "float myVarC", "", "", ""], ["arr myFunc2", "double otherVarA", "bool otherVarB", "", "", "", ""]], source_parser.parse_signature("int myFunc1(bool myVarA, String myVarB, float myVarC) {\nx++;\n}\n    arr myFunc2( double otherVarA, bool otherVarB)\n{\n}", 6))
    def test_stuff_in_between(self):
        self.assertListEqual([["int myFunc1", "bool myVarA", "String myVarB", "float myVarC", "", "", ""], ["arr myFunc2", "double otherVarA", "bool otherVarB", "", "", "", ""]], source_parser.parse_signature("int myFunc1(bool myVarA, String myVarB, float myVarC) {\nx++;\n}\n  //there's just a comment here\n  arr myFunc2( double otherVarA, bool otherVarB)\n{\n}", 6))