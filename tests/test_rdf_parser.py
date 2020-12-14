from rdf_parser.rdf_parser import RdfParser
from resources import knox_triples


class TestRdfParser:
    def setup_method(self):
        self.rdf_parser = RdfParser("file://testing.namespace.dk/")

    def test_should_be_able_to_add_triple(self):
        self.rdf_parser.add_rdf_triple(knox_triples.MetaDataTriple("Title of manual"))
        assert len(self.rdf_parser.rdf_graph) == 1
