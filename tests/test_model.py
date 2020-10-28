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

    def test_detect_dependency_nsubj(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        apple = self.model.tokens()[0]

        assert apple.dep == Dependency.nsubj

    def test_detect_dependency_aux(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        _is = self.model.tokens()[1]

        assert _is.dep == Dependency.aux

    def test_detect_dependency_root(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        looking = self.model.tokens()[2]

        assert looking.dep == Dependency.root

    def test_detect_dependency_prep(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        at = self.model.tokens()[3]

        assert at.dep == Dependency.prep

    def test_detect_dependency_pcomp(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        buying = self.model.tokens()[4]

        assert buying.dep == Dependency.pcomp

    def test_detect_dependency_compund(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        UK = self.model.tokens()[5]

        assert UK.dep == Dependency.compound

    def test_detect_dependency_dobj(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        startup = self.model.tokens()[6]

        assert startup.dep == Dependency.dobj

    def test_detect_dependency_quantmod(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        dollar = self.model.tokens()[8]

        assert dollar.dep == Dependency.quantmod

    def test_detect_dependency_pobj(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        billion = self.model.tokens()[10]

        assert billion.dep == Dependency.pobj