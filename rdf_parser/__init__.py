from rdflib import URIRef
from rdflib.namespace import ClosedNamespace

GRUNDFOS = ClosedNamespace(
    uri=URIRef("grundfos/", "http://www.knoxproject.aau.dk/"),
    terms=[
        "Manual", "Organisation", "Author", "publishes", "Date", "Publisher", "Page",
        "Section", "Unit", "the_pump", "isWrittenBy", "isPublishedBy", "isPublishedAt", "mentionedOn",
        "isInSection", "Title", "Link", "Name", "PublicationDate", "pageNumber",
        "sectionTitle"]
)
