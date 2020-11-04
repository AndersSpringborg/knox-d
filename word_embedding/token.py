from word_embedding.grammarcategories import GrammarCategories
from word_embedding.dependency import Dependency


class Token:
    """
    Class token is implementation of token for the word embeddings
    """
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
