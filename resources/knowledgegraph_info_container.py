from typing import List
from resources.json_wrapper import Manual


class KnowledgeGraphInfo:
    """
    Data-structure for the information needed to construct a knowledge graph object
    """
    sentences: List[list]
    manual: Manual

    def __init__(self, _sentences=None, _manual=None):
        self.sentences = _sentences
        self.manual = _manual
