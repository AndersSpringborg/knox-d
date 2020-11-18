from collections import Counter


class TermFrequency:
    """
    A module that count the term frequency.

    It is used by processing strings, where a doc title is given, and the string is given
    The text is expected to be preprocessed

    ex.
    tf = TermFrequency()
    tf.process(doc.title, doc.corpus)

    Then it can accessed like a hashtable

    tf.terms[word] gives an array of the documents it is found in.
    tf[doc_title] gives a hashtable where the key is term, and the value is frequency
    """
    def __init__(self):
        self.terms = {}
        self.__doc = {}

    def __getitem__(self, key):
        if key not in self.__doc.keys():
            self.__doc[key] = DocCounter()
        return self.__doc[key]

    def process(self, doc_title: str, sentence: str):
        """
        Process text, given a document title
        """
        for term in sentence.split(' '):
            self[doc_title].length += 1
            self[doc_title][term] += 1

            if term not in self.terms.keys():
                self.terms[term] = []
            self.terms[term].append(doc_title)


class DocCounter(Counter):  # pylint: disable=W0223
    # Abstract method is not overwritten. The Counter object, choose, not to implement it.
    """
    A counter object with a added length and vocab var
    """
    def __init__(self, *args, **kwargs):
        self.length = 0
        super().__init__(*args, **kwargs)

    @property
    def vocab(self):
        return len(self.keys())
