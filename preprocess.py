import logging
import os
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from nltk.tokenize import sent_tokenize

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class CleanSentence(object):
    def __init__(self, dirname):
        self.dirname = dirname
        self.sentence_count = 0

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, fname)) as f_input:
                corpus = f_input.read()
            raw_sentences = sent_tokenize(corpus)
            for sentence in raw_sentences:
                if len(sentence) > 0:
                    self.sentence_count += 1
                    yield simple_preprocess(sentence)

