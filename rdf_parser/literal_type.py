from enum import Enum
from rdflib.namespace import XSD
from enum_switch import Switch

class LiteralType(Enum):
    STRING = 1
    DATE = 2
    INT = 3

class LiteralTypeSwitch(Switch):
    def STRING(self):
        return XSD.string

    def DATE(self):
        return XSD.date

    def INT(self):
        return XSD.int