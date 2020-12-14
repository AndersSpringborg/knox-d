from abc import ABC

from rdflib.term import Node

from rdf_parser import rdf_helper, GRUNDFOS


class Triple(ABC):
    """
    Data-structure for the relation data (subject, object, relation), used with the knowledge graph
    """

    def subj_(self) -> Node:
        pass

    def rel_(self) -> Node:
        pass

    def obj_(self) -> Node:
        pass

    def parse(self):
        return self.subj_(), self.rel_(), self.obj_()

    def term(self, namespace, term):
        return rdf_helper.get_term(namespace, term)

    def literal(self, string: str, literal_type: str):
        return rdf_helper.generate_rdf_literal(string, literal_type)

    def blank_node(self, string: str):
        return rdf_helper.generate_rdf_blank_node(string)

    def __repr__(self):
        return "<" + str(self.subj_()) + "> " + "<" + str(self.rel_()) + "> " + "<" + str(self.obj_()) + ">"


class StringTriple(Triple):
    """
    A triple where everything is strings
    """

    def __init__(self, _subj: str, _rel: str, _obj: str):
        self.subj = _subj
        self.obj = _obj
        self.rel = _rel


class MetaDataTriple(Triple):
    """
    The default triple for metadata
    """

    def __init__(self, title):
        self.manual_uri = rdf_helper.generate_rdf_uri_ref(GRUNDFOS.uri,
                                                          ref=title,
                                                          sub_uris=["manual"])

    def subj_(self):
        return self.manual_uri

    def rel_(self):
        return self.term("rdf", "type")

    def obj_(self):
        return self.term("grundfos", "Manual")

    def __repr__(self):
        return "<" + str(self.subj_()) + "> " + "<" + str(self.rel_()) + "> " + "<" + str(self.obj_()) + ">"


class PublishTriple(MetaDataTriple):
    """
    Define about the publisher of an article
    """

    def __init__(self, title: str, publisher: str = ''):
        super().__init__(title)
        self.publisher = publisher

    def subj_(self):
        return self.manual_uri

    def rel_(self):
        return self.term("grundfos", "isPublishedBy")

    def obj_(self):
        return self.literal(self.publisher, "string")

    def __repr__(self):
        return "<" + str(self.subj_()) + "> " + "<" + str(self.rel_()) + "> " + "\"" + str(self.obj_()) + "\""


class PublishedAtTriple(PublishTriple):
    """
    Define when a article is published
    """

    def __init__(self, title: str, published_at: str):
        super().__init__(title)
        self.published_at = published_at

    def rel_(self):
        return self.term("grundfos", "isPublishedAt")

    def obj_(self):
        return self.literal(self.published_at, "date")


class TitleTriple(MetaDataTriple):
    """
    Define a title of a manual
    """

    def __init__(self, title):
        super().__init__(title)
        self.title = title

    def rel_(self):
        return self.term("grundfos", "Title")

    def obj_(self):
        return self.literal(self.title, "date")

    def __repr__(self):
        return "<" + str(self.subj_()) + "> " + "<" + str(self.rel_()) + "> " + "\"" + str(self.obj_()) + "\""


class SectionTriple(Triple):
    """
    Define a section
    """

    def __init__(self, section_uri, section_title):
        self.section_uri = section_uri
        self.section_title = section_title

    def subj_(self):
        return self.section_uri

    def rel_(self):
        return self.term("rdf", "type")

    def obj_(self):
        return self.term("grundfos", "Section")


class PageTriple(Triple):
    """
    Define a page
    """

    def __init__(self, page_uri, page_number):
        self.page_uri = page_uri
        self.page_number = page_number

    def subj_(self):
        return self.page_uri

    def rel_(self):
        return self.term("rdf", "type")

    def obj_(self):
        return self.term("grundfos", "Page")


class PageInSectionTriple(Triple):
    """
    Defines a relation between a page and a section
    """

    def __init__(self, page_uri, section_uri):
        self.page_uri = page_uri
        self.section_uri = section_uri

    def subj_(self):
        return self.page_uri

    def rel_(self):
        return self.term("grundfos", "isInSection")

    def obj_(self):
        return self.section_uri


class SentenceTriple(Triple):
    """
    Defines triples that extract knowledge from the triple
    """

    def __init__(self, subj, rel, obj):
        self.subj = subj
        self.rel = rel
        self.obj = obj

    def subj_(self):
        return self.term("grundfos", self.subj)

    def rel_(self):
        return self.term("grundfos", self.rel)

    def obj_(self):
        try:
            term = self.term("grundfos", self.obj)
        except KeyError:
            term = self.blank_node(self.obj)
        return term
