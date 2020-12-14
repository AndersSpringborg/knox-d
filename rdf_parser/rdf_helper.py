from rdflib import RDF, RDFS, OWL, XSD, BNode, URIRef, Literal

from rdf_parser import GRUNDFOS
from resources.error import error


def get_term(namespace, term):
    """ Finds and return a closed namespace term when given a string and a namespace

    Make sure the term is within the namespaces.
    Parameters
    ----------
    namespace : str
        Namespace containing the wanted term
    term : str
        Term to find in given namespace

    Raises
    ------
    Exception
        Could not find namespace

    Returns
    -------
    closed_namespace_term
        A closed namespace term
    """
    if namespace == "rdf":
        return RDF.term(term)
    if namespace == "rdfs":
        return RDFS.term(term)
    if namespace == "owl":
        return OWL.term(term)
    if namespace == "xsd":
        return XSD.term(term)
    if namespace == "grundfos":
        return GRUNDFOS.term(term)

    raise Exception("Namespace not found")


def generate_rdf_blank_node(value=None):
    """ Returns a RDF BlankNode (BNode)

    Returns
    -------
    BNode
        A RDF BlankNode. Can only be used to as Object and Subject in an RDF Triple.
    """
    return BNode(value)


def generate_rdf_uri_ref(namespace_base, ref, sub_uris: list):
    """ Returns a new URI reference

    Parameters
    ----------
    ref : str
        Reference to RDF Object
    sub_uris : array of str
        Sub URI's of the reference e.g. ["manual", "section"]
    namespace_base : The base of the namespace used to generate the UriRef
        An example is "https://knox-project.aau.dk"

    Returns
    -------
    URIRef
        A URIRef to the RDF Object

    Example
    -------
    generate_rdf_uri_ref("section xzy", ["manual", "section"])
    # Returns the URIRef -> "file://testnamepace.org/manual/section/section_xzy"
    """
    if not ref:
        return generate_rdf_blank_node()

    uri_builder = ""

    for uri in sub_uris:
        if not uri:
            continue
        uri_builder += uri + "/"

    uri_builder += ref
    uri_builder = uri_builder.replace(" ", "_")

    return URIRef(namespace_base + uri_builder)


def generate_rdf_literal(value: str, literal_type: str) -> Literal:
    if value in "" or value is None:
        error("Empty value in rdf literal is not supported")
        raise RdfHelperException()

    if literal_type in "string":
        return Literal(value.replace(" ", "_"), datatype=XSD.string)

    if literal_type in "date":
        return Literal(value, datatype=XSD.date)

    if literal_type in "integer":
        return Literal(value, datatype=XSD.int)

    raise TypeError()


class RdfHelperException(Exception):
    """
    wrapper to rdf exception, so we don't depend on that library
    """
