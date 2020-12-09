from abc import ABC

from rdflib.term import Node

from rdf_parser.literal_type import LiteralType
from rdf_parser.rdf_parser import RdfParser


class Triple(ABC):
    """
    Data-structure for the relation data (subject, object, relation), used with the knowledge graph
    """
    subj = ''
    obj = ''
    rel = ''

    def __init__(self, _subj, _rel, _obj):
        self.subj = _subj
        self.obj = _obj
        self.rel = _rel

    def subj_(self) -> Node:
        pass

    def rel_(self) -> Node:
        pass

    def obj_(self) -> Node:
        pass

    def parse(self):
        return (self.subj_(), self.obj_(), self.rel_())

    def term(self, namespace, term):
        return RdfParser.get_term(namespace, term)

    def literal(self, string, type):
        return RdfParser.generate_rdf_literal(string, type)


class MetaDataTriple(Triple):
    def __init__(self, title):
        self.manual_uri = RdfParser.generate_rdf_uri_ref(ref=title, sub_uris=["manual"])


class PublishTriple(MetaDataTriple):
    def __init__(self, title: str, publisher: str = ''):
        super().__init__(title)
        self.publisher = publisher

    def subj_(self):
        return self.manual_uri

    def rel_(self):
        return self.term("grundfos", "publishedBy")

    def obj_(self):
        return self.literal(self.publisher, LiteralType.STRING)


class PublishedAtTriple(PublishTriple):
    def __init__(self, published_at: str, title):
        super().__init__(title)
        self.publishedAt = published_at

    def subj_(self):
        return super().subj_()

    def rel_(self):
        return self.literal(self.publishedAt, LiteralType.DATE)

    def obj_(self):
        return self.term("grundfos", "publishedAt")


class TitleTriple(MetaDataTriple):
    def __init__(self, title):
        super().__init__(title)
        self.title = title

    def subj_(self):
        return super().subj_()

    def rel_(self):
        return self.term("grundfos", "Title")

    def obj_(self):
        return self.literal(self.title, LiteralType.STRING)
