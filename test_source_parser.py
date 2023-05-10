from unittest import TestCase
import source_parser

class ParserTestCase(TestCase):
    def test_simple_params(self):
        self.assertListEqual([["int myFunc", "bool myVarA", "String myVarB"]], source_parser.parse_signature("int myFunc(bool myVarA, String myVarB) {"))