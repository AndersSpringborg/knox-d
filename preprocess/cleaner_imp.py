import spacy
import re
import time
import pandas as pd
from preprocess.cleaner import Cleaner
import nltk


class CleanerImp(Cleaner):

    def bigrams(self, words: str) -> [tuple]:
        word_tokens = nltk.word_tokenize(words)
        bigram_tokens = nltk.bigrams(word_tokens)

        return list(bigram_tokens)

    def to_lower(self, words):
        return words.lower()

    def remove_special_characters(self, txt):
        cleaned_text = re.sub("[^a-zA-Z ]", '', txt)
        return cleaned_text

    def numbers_to_text(self, text):
        result = ""

        for token in text.split():
            if token.isdigit():
                result += self._textify_token(token)
            else:
                result += token
            result += " "

        return result.strip()

    def _textify_token(self, token):
        result = ""
        for digit in token:
            result += self._textify_number(digit)
            result += " "

        return result.strip()

    def _textify_number(self, digit):
        numbers = {
            '0': 'zero',
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five',
            '6': 'six',
            '7': 'seven',
            '8': 'eight',
            '9': 'nine'
        }
        return numbers[digit]

    def remove_duplicates(self, str_list):
        return list(set(str_list))

    def lemmatize(self, word):
        # Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

        doc = nlp(word)

        return " ".join([token.lemma_ for token in doc])

# Tasks:
#
# Should $ be converted to " dollar" ??
