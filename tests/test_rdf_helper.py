import pytest
from rdflib import term, BNode, Literal, XSD

from rdf_parser import rdf_helper
from rdf_parser.rdf_helper import RdfHelperException


class TestRdfHelper:
    def setup_method(self):
        self.namespace = "file://testing.namespace.dk/"

    def test_can_get_term(self):
        rdf_helper.get_term("rdf", "type")

    def test_can_generate_blank_node(self):
        blank_node = rdf_helper.generate_rdf_blank_node()
        assert isinstance(blank_node, BNode)

    def test_should_generate_correct_uriref(self):
        uri_ref = rdf_helper.generate_rdf_uri_ref(self.namespace, "name of unit", ["manual"])
        assert uri_ref == term.URIRef("file://testing.namespace.dk/manual/name_of_unit")

    def test_generate_correct_uriref_no_suburis(self):
        uri_ref = rdf_helper.generate_rdf_uri_ref(self.namespace, "some_title", [])
        assert uri_ref == term.URIRef("file://testing.namespace.dk/some_title")

    def test_generate_correct_uriref_empty_suburis(self):
        uri_ref = rdf_helper.generate_rdf_uri_ref(self.namespace, "some_title", [""])
        assert uri_ref == term.URIRef("file://testing.namespace.dk/some_title")

    def test_raise_exception_if_ref_is_empty(self):
        uri_ref = rdf_helper.generate_rdf_uri_ref(self.namespace, "", ["manual"])
        assert isinstance(uri_ref, BNode)

    def test_should_generate_correct_rdf_literal(self):
        literal = rdf_helper.generate_rdf_literal("Some String", "string")
        assert isinstance(literal, Literal)
        assert literal.datatype == XSD.string

        literal = rdf_helper.generate_rdf_literal("Some String", "date")

        assert isinstance(literal, Literal)
        assert literal.datatype == XSD.date

        literal = rdf_helper.generate_rdf_literal("Some String", "integer")

        assert isinstance(literal, Literal)
        assert literal.datatype == XSD.int

    def test_should_raise_rdf_helper_exception_on_empty_string(self):
        with pytest.raises(RdfHelperException):
            literal = rdf_helper.generate_rdf_literal("", "string")