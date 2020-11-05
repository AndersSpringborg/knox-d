import spacy
from word_embedding.grammarcategories import GrammarCategories
from word_embedding.converter import Converter
from word_embedding.token import Token


class SpacyModel:
    """
    This is a implementations of the abstract class model, using spacy
    """
    def load(self, sentence: str):
        self.words = sentence
        self.spacytokens = self.model(sentence)

    def __init__(self):
        self.model = spacy.load("en_core_web_sm")
        self.spacytokens = None

    words = ""
    keyvector = ""

    def tokens(self):
        doc = list(self.spacytokens.sents)
        sentences = []

        for sentence in doc:
            sentences.append(self.__convert_tokens(sentence))

        return sentences

    def __convert_tokens(self, sentence):
        list_of_tokens = []

        for spacy_token in sentence:
            name = spacy_token.text
            pos_tag = self.get_pos_tag_from_spacytoken(spacy_token)
            dependency = self.get_dependency_from_spacytoken(spacy_token)

            new_token = Token(name, pos_tag, dependency)
            list_of_tokens.append(new_token)

        return list_of_tokens

    def get_dependency_from_spacytoken(self, spacy_token):
        spacy_dependency = spacy_token.dep_
        return Converter.dependency(spacy_dependency)

    def get_pos_tag_from_spacytoken(self, spacy_token):
        space_pos_tag = spacy_token.tag_
        converter = {
            "NN": GrammarCategories.noun,
            "JJ": GrammarCategories.adj,
            "NNP": GrammarCategories.noun}
        if space_pos_tag not in converter.keys():
            return GrammarCategories.other

        return converter[space_pos_tag]
