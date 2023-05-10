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