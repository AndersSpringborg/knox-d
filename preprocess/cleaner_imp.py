import re
import spacy
from preprocess.cleaner import Cleaner


class CleanerImp(Cleaner):
    """
    First implementation of super class
    """

    def bigrams(self, sentence: str) -> str:
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(sentence)

        for noun_phrase in list(doc.noun_chunks):
            if noun_phrase.string.endswith(' '):
                bigram = noun_phrase.string
                # Remove trailing whitespace in noun_phrase to avoid:
                # "ice cream " --> "ice_cream_"
                # Insted of "ice cream " --> "ice_cream "
                bigram = bigram.strip(' ')
                bigram = bigram.replace(' ', '_')
                bigram += ' '
            else:
                bigram = noun_phrase.string
                bigram = bigram.strip(' ')
                bigram = bigram.replace(' ', '_')

            sentence = sentence.replace(noun_phrase.string, bigram)

        return sentence

    def to_lower(self, words):
        return words.lower()

    def remove_special_characters(self, txt):
        cleaned_text = re.sub("[^a-zA-Z. ]", '', txt)
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

    def lemmatize(self, words: str):
        # Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

        doc = nlp(words)

        return " ".join([token.lemma_ for token in doc])


    def insert_pump_name(self, data, pump_name):
        data = data.replace("the_pump", pump_name)
        return data


# Tasks:
#
# Should $ be converted to " dollar" ??
