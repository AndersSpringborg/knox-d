from word_embedding.Model import Model
import spacy


class Spacy(Model):

    model: spacy

    def __init__(self):
        pass

    def load(self, path):
        self.model = spacy.load(path)

    def update(self):
        pass

    def save(self, path):
        self.model.to_disk(path)
        pass
