from rdflib import Graph, Literal, RDF, URIRef, BNode
from rdflib.namespace import XSD, RDFS, ClosedNamespace, OWL

from rdf_parser import GRUNDFOS
from resources.error import error


class RdfParser:
    """
    Used for parsing custom namespace and ontology,
    this allows using relationships that works for the custom contexts.
    For the KNOX project it would either be Grundfos or Nordjyske.

    Methods
    -------
    use_ontology_from_path(file_path, file_ext)
        This method loads a given ontology and parses it to a specified format.
        If no file_ext is specified, the default is "ttl" (turtle)

    Attributes
    ----------
    self.GRUNDFOS : rdflib.ClosedNamespace
        Namespace for the context of Grundfos, it contains the relevant relations as well as types
    self.rdf_graph : rdflib.Graph
        Holds the entire graph, in this case it is the knowledge graph for Grundfos.
    """
    rdf_graph = Graph()

    def __init__(self, namespace_base="http://www.knoxproject.aau.dk/"):
        self.rdf_graph = Graph()
        self.rdf_graph.bind("grundfos", GRUNDFOS)
        self.rdf_graph.bind("rdf", RDF)
        self.rdf_graph.bind("rdfs", RDFS)
        self.rdf_graph.bind("owl", OWL)
        self.namespace_base = namespace_base

    def add_rdf_triple(self, rdf_triple):
        try:
            triple = rdf_triple.parse()
            self.rdf_graph.add(triple)
        except KeyError as err:
            error("the key is wrong", err)

    def store_knowledge_graph(self, output_folder_path, output_file_name, output_format):
        """Stores the knowledge graph in a file in a user specified location.

        Parameters
        ----------
        output_file_name : str
            Specify the output file name
        output_folder_path : str
            Specify the wanted output folder - this stores the knowledge graph locally.
        output_format : str
            Specify the output format for the knowledge graph to be saved as.
        """
        self.rdf_graph.serialize(format=output_format,
                                 destination=output_folder_path + output_file_name + "." + output_format,
                                 encoding="utf-8")

    def pretty_print_knowledge_graph(self):
        """This method is used to print out the knowledge graph in a human readable way.

        Be aware that it goes through every triple in the knowledge graph
        """
        print(self.rdf_graph.serialize(format="turtle").decode("utf-8"))
