import pytest
from word_embedding.grammarcategories import GrammarCategories
from word_embedding.spacy_model import SpacyModel
from word_embedding.token import Token
from word_embedding.dependency import Dependency


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

        assert token in tokens[0]

    def test_token_has_label(self):
        self.model.load("apple")

        first_sentance= self.model.tokens()[0]
        token = first_sentance.pop()

        assert token.pos_tag == GrammarCategories.noun

    def test_token_can_have_adj_label(self):
        self.model.load("good")

        first_sentance = self.model.tokens()[0]
        token =  first_sentance.pop()

        assert token.pos_tag == GrammarCategories.adj

    def test_token_out_of_category(self):
        self.model.load("tyggegummi")

        tokens = self.model.tokens()
        token = tokens[0].pop()

        assert token.pos_tag == GrammarCategories.other

    def test_detect_dependency_nsubj(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        tokens = self.model.tokens()
        apple = tokens[0][0]

        assert apple.dep == Dependency.nsubj

    def test_detect_dependency_aux(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        tokens = self.model.tokens()
        _is = tokens[0][1]

        assert _is.dep == Dependency.aux

    def test_detect_dependency_root(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        first_sentance= self.model.tokens()[0]
        looking = first_sentance[2]

        assert looking.dep == Dependency.root

    def test_detect_dependency_prep(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        first_sentance= self.model.tokens()[0]
        at = first_sentance[3]

        assert at.dep == Dependency.prep

    def test_detect_dependency_pcomp(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        first_sentance= self.model.tokens()[0]
        buying = first_sentance[4]

        assert buying.dep == Dependency.pcomp

    def test_detect_dependency_compund(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        first_sentance= self.model.tokens()[0]
        UK = first_sentance[5]

        assert UK.dep == Dependency.compound

    def test_detect_dependency_dobj(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        first_sentance= self.model.tokens()[0]
        startup = first_sentance[6]

        assert startup.dep == Dependency.dobj

    def test_detect_dependency_quantmod(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        tokens = self.model.tokens()
        dollar = tokens[0][8]

        assert dollar.dep == Dependency.quantmod

    def test_detect_dependency_pobj(self):
        self.model.load("Apple is looking at buying U.K. startup for $1 billion")

        tokens = self.model.tokens()
        billion = tokens[0][10]

        assert billion.dep == Dependency.pobj

    def test_can_split_text_into_one_list_per_sentence(self):
        self.model.load("I like apples. He likes apples. She likes Apples.")

        tokens = self.model.tokens()

        i = tokens[0][0]
        assert i.name == "I"

        he = tokens[1][0]
        assert he.name == "He"

        she = tokens[2][0]
        assert she.name == "She"

    def test_can_split_text_into_one_list_per_sentence_no_punctuation(self):
        self.model.load("i like apples. he likes apples. she likes apples")

        tokens = self.model.tokens()

        i = tokens[0][0]
        assert i.name == "i"

        he = tokens[1][0]
        assert he.name == "he"

        she = tokens[2][0]
        assert she.name == "she"
