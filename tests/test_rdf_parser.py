import rdf_parser
import pytest
from rdflib import Graph, Literal, RDF, URIRef, BNode, term
from rdf_parser.rdf_parser import RdfParser
from rdf_parser.literal_type import LiteralType
import os

class TestRdfParser:
    def setup_method(self):
        self.rdf_parser = RdfParser("file://testing.namespace.dk/")


    def test_should_be_able_to_add_triple(self):
        self.rdf_parser.add_rdf_triple(
            (self.rdf_parser.generate_rdf_literal("this is", LiteralType.STRING),
            self.rdf_parser.generate_rdf_literal("an example", LiteralType.STRING),
            self.rdf_parser.generate_rdf_literal("triple", LiteralType.STRING)))
        assert len(self.rdf_parser.rdf_graph) == 1

    def should_not_add_if_one_is_empty_triple(self):
        self.rdf_parser.add_rdf_triple((None, None, None))
        self.rdf_parser.add_rdf_triple((self.rdf_parser.generate_rdf_uri_ref("name of unit", ["manual"]), None, None))
        self.rdf_parser.add_rdf_triple((None, self.rdf_parser.generate_rdf_literal("Test literal"), None))
        self.rdf_parser.add_rdf_triple((None, None, self.rdf_parser.generate_rdf_literal("Test literal")))
        assert len(self.rdf_parser.rdf_graph) == 0

    def test_should_generate_correct_uriref(self):
        uri_ref = self.rdf_parser.generate_rdf_uri_ref("name of unit", ["manual"])
        assert uri_ref == term.URIRef("file://testing.namespace.dk/manual/name_of_unit")

    def test_generate_correct_uriref_no_suburis(self):
        uri_ref = self.rdf_parser.generate_rdf_uri_ref("some_title", [])
        assert uri_ref == term.URIRef("file://testing.namespace.dk/some_title")

    def test_generate_correct_uriref_empty_suburis(self):
        uri_ref = self.rdf_parser.generate_rdf_uri_ref("some_title", [""])
        assert uri_ref == term.URIRef("file://testing.namespace.dk/some_title")

    def test_raise_exception_if_ref_is_empty(self):
        uri_ref = self.rdf_parser.generate_rdf_uri_ref("", ["manual"])
        assert isinstance(uri_ref, BNode)
