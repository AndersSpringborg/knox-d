from collections import Counter


class TermFrequency:
    def __init__(self):
        self.terms = {}

    def __getitem__(self, key):
        if key not in self.terms.keys():
            self.terms[key] = Counter()
        return self.terms[key]

    def process(self, doc: str, sentence: str):
        for term in sentence.split(' '):
            self[doc][term] += 1

            if term not in self.terms.keys():
                self.terms[term] = []
            self.terms[term].append(doc)
