

class KnowledgeGraph:
    triples = []
    sentences = []
    vocab: object
    def __init__(self, _sentences):
        self.sentences = _sentences
        self.construct_triples()

    def construct_triples(self):
        for sentence in self.sentences:
            subject_object_pairs = self.get_subject_and_object_pair(sentence)
            relation = self.get_subject_and_object_relations(sentence)
            self.triples.append((subject_object_pairs[0], relation, subject_object_pairs[1]))

    def get_subject_and_object_pair(self, sentence: list):
        subj = ''
        obj = ''
        for token in sentence:
            if token.dep_.find("subj"):
                subj = token.text
            elif token.dep_.find("obj"):
                obj = token.text
            else:
                continue
        return subj, obj

    def get_subject_and_object_relations(self, sentences):
        relation = ""

        return relation