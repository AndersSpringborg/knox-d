from enum import Enum, auto
import spacy
from tokencontainer import GrammarCategories


class SpacyModel:
    def load(self, sentence: str):
        self.words = sentence
        self.spacytokens = self.model(sentence)

    def __init__(self):
        self.model = spacy.load("en_core_web_sm")
        self.spacytokens = None

    words = ""
    keyvector = ""

    def tokens(self):
        list_of_tokens = []
        for spacy_token in self.spacytokens:
            name = spacy_token.text
            pos_tag = self.get_pos_tag_from_spacytoken(spacy_token)
            dependency = self.get_dependency_from_spacytoken(spacy_token)

            new_token = Token(name, pos_tag, dependency)
            list_of_tokens.append(new_token)
        return list_of_tokens

    def get_dependency_from_spacytoken(self, spacy_token):
        spacy_dependency = spacy_token.dep_
        return Converter.dependency(spacy_dependency)

    def get_pos_tag_from_spacytoken(self, spacy_token):
        space_pos_tag = spacy_token.tag_
        converter = {
            "NN": GrammarCategories.noun,
            "JJ": GrammarCategories.adj,
            "NNP": GrammarCategories.noun}
        if space_pos_tag not in converter.keys():
            return GrammarCategories.other
        else:
            return converter[space_pos_tag]


class Dependency(Enum):
    root = auto()
    nsubj = auto()
    acl = auto()
    acomp = auto()
    advcl = auto()
    advmod = auto()
    agent = auto()
    amod = auto()
    appos = auto()
    attr = auto()
    aux = auto()
    auxpass = auto()
    case = auto()
    cc = auto()
    ccomp = auto()
    compound = auto()
    conj = auto()
    cop = auto()
    csubj = auto()
    csubjpass = auto()
    dative = auto()
    dep = auto()
    det = auto()
    dobj = auto()
    expl = auto()
    intj = auto()
    mark = auto()
    meta = auto()
    neg = auto()
    nn = auto()
    nounmod = auto()
    npmod = auto()
    nsubjpass = auto()
    nummod = auto()
    oprd = auto()
    obj = auto()
    obl = auto()
    parataxis = auto()
    pcomp = auto()
    pobj = auto()
    poss = auto()
    preconj = auto()
    prep = auto()
    prt = auto()
    punct = auto()
    quantmod = auto()
    relcl = auto()
    xcomp = auto()
    other = auto()


class Token:
    pos_tag: GrammarCategories
    dep: Dependency
    name = ""

    def __init__(self, name, pos_tag=None, dep=None):
        self.name = name
        self.pos_tag = pos_tag
        self.dep = dep

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f"Token: name:{self.name}"


class Converter():
    @staticmethod
    def dependency(dep: str) -> Dependency:
        converter = {
            "nsubj": Dependency.nsubj,
            "pobj": Dependency.pobj,
            "aux": Dependency.aux,
            "ROOT": Dependency.root,
            "prep": Dependency.prep,
            "pcomp": Dependency.pcomp,
            "compound": Dependency.compound,
            "dobj": Dependency.dobj,
            "quantmod": Dependency.quantmod,
        }

        if dep not in converter.keys():
            return Dependency.other
        else:
            return converter[dep]
