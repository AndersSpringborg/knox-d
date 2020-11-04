from enum import Enum, auto

class GrammarCategories(Enum):
    """
    Grammatical categories for knox data
    """
    subj = auto()
    obj = auto()
    rel = auto()
    adj = auto()
    noun = auto()
    other = auto()
