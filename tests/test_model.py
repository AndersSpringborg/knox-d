import pytest
import spacy
from tokencontainer import GrammarCategories
from word_embedding.spacy_model import SpacyModel, Token, Dependency


class TestModel:

    def setup_method(self):
        self.model = SpacyModel()

    def test_load_test_into_model_produce_keyvectors(self):
        cleaned_sentence = "original safety instruction"
        self.model.load(cleaned_sentence)
        assert self.model.keyvector is not None

    def test_spacy_model_exists(self):
        assert self.model is not None

    def test_input_sentence_in_tokens(self):
        cleaned_sentence = "original safety instruction"
        self.model.load(cleaned_sentence)

        token = Token("original")
        tokens = self.model.tokens()
        assert token in tokens

    def test_token_has_label(self):
        self.model.load("apple")
        token = self.model.tokens().pop()
        assert token.pos_tag == GrammarCategories.noun

    def test_token_can_have_adj_label(self):
        self.model.load("good")
        token = self.model.tokens().pop()
        assert token.pos_tag == GrammarCategories.adj

    def test_token_out_of_category(self):
        self.model.load("tyggegummi")
        token = self.model.tokens().pop()
        assert token.pos_tag == GrammarCategories.other

    def test_detect_dependencies(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        apple = self.model.tokens()[0]
        assert apple.dep == Dependency.nsubj