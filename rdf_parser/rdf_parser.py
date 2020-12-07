from rdflib import Graph, Literal, RDF, URIRef, BNode
from rdflib.namespace import XSD, RDFS, ClosedNamespace, OWL
from rdf_parser.literal_type import LiteralType, LiteralTypeSwitch


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

    GRUNDFOS = ClosedNamespace(
        uri=URIRef("grundfos/", "http://www.knoxproject.aau.dk/"),
        terms=[
            "Manual", "Organisation", "Author", "publishes", "Date", "Publisher", "Page",
            "Section", "Unit", "Pump", "isWrittenBy", "isPublishedBy", "isPublishedAt", "mentionedOn",
            "isInSection", "Title", "Link", "Name", "PublicationDate", "pageNumber",
            "sectionTitle", "be", "develop"]
    )

    def __init__(self, namespace_base="http://www.knoxproject.aau.dk/"):
        self.rdf_graph = Graph()
        self.rdf_graph.bind("grundfos", self.GRUNDFOS)
        self.rdf_graph.bind("rdf", RDF)
        self.rdf_graph.bind("rdfs", RDFS)
        self.rdf_graph.bind("owl", OWL)
        self.namespace_base = namespace_base

    def add_rdf_triple(self, rdf_triple):
        if rdf_triple[0] and rdf_triple[1] and rdf_triple[2]:
            self.rdf_graph.add(rdf_triple)

    @staticmethod
    def generate_rdf_literal(value, literalType: LiteralType = LiteralType.STRING):
        switch = LiteralTypeSwitch(LiteralType)
        return Literal(value.replace(" ", "_"), datatype=switch(literalType))

    def generate_rdf_uri_ref(self, ref, sub_uris):
        """ Returns a new URI reference

        Parameters
        ----------
        ref : str
            Reference to RDF Object
        sub_uris : array of str
            Sub URI's of the reference e.g. ["manual", "section"]

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
            return self.generate_rdf_blank_node()

        full_ref = self.namespace_base

        for uri in sub_uris:
            if not uri:
                continue
            full_ref += uri + "/"

        full_ref += ref

        return URIRef(full_ref.replace(" ", "_"))

    def store_knowledge_graph(self, output_folder_path, file_name, output_format):
        """Stores the knowledge graph in a file in a user specified location.

        Parameters
        ----------
        output_folder_path : str
            Specify the wanted output folder - this stores the knowledge graph locally.
        output_format : str
            Specify the output format for the knowledge graph to be saved as.
        """
        self.rdf_graph.serialize(format=output_format,
                                 destination=output_folder_path + file_name + "." + output_format,
                                 encoding="utf-8")

    def pretty_print_knowledge_graph(self):
        """This method is used to print out the knowledge graph in a human readable way.

        Be aware that it goes thorugh every triple in the knowledge graph
        """
        print(self.rdf_graph.serialize(format="turtle").decode("utf-8"))

        # for triple in self.knowledge_graph:
        #     pprint.pprint(triple)

    def get_term(self, namespace, term):
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
        closednamespaceterm
            A closed namespace term
        """
        try:
            if namespace == "rdf":
                return RDF.term(term)
            elif namespace == "rdfs":
                return RDFS.term(term)
            elif namespace == "owl":
                return OWL.term(term)
            elif namespace == "xsd":
                return XSD.term(term)
            elif namespace == "grundfos":
                return self.GRUNDFOS.term(term)
            else:
                raise Exception("Namespace not found")
        except Exception:
            return None

    @staticmethod
    def generate_rdf_blank_node():
        """ Returns a RDF BlankNode (BNode)

        Returns
        -------
        BNode
            A RDF BlankNode. Can only be used to as Object and Subject in an RDF Triple.
        """
        return BNode()
