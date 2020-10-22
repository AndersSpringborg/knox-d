from enum import Enum, auto

class GrammarCategories(Enum):
    subj = auto()
    obj = auto()
    rel = auto()
    adj = auto()
    noun = auto()
    other = auto()


class Token:
    def __init__(self, _name, _cluster_cat):
        self.name = _name
        self.cluster_cat = _cluster_cat

    # The word
    name = ''
    # The category from the cluster
    cluster_cat = ''
    # Grammatical category used in the knowledge graph. Must be of type grammar_categories
    grammar_cat: GrammarCategories

    # The grammar_cat can be decided on behalf of the cluster_cat. i.e:
    # Two clusters containing relation words might be called REL1 and REL2
    # Find the tokens with cluster_cat = REL 1 || REL 2 and set grammar_cat to grammar_categories.rel




