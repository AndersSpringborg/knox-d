class Triple:
    """
    Data-structure for the relation data (subject, object, relation), used with the knowledge graph
    """
    subj = ''
    obj = ''
    rel = ''

    def __init__(self, _subj, _rel, _obj):
        self.subj = _subj
        self.obj = _obj
        self.rel = _rel
