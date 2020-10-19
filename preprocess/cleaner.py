import spacy
import re
import time
import pandas as pd

class Cleaner:
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
            '0' : 'zero',
            '1' : 'one',
            '2' : 'two',
            '3' : 'three',
            '4' : 'four',
            '5' : 'five',
            '6' : 'six',
            '7' : 'seven',
            '8' : 'eight',
            '9' : 'nine'
        }
        return numbers[digit]

    def remove_duplicates(self, str_list):
        return list(set(str_list))


    def lemmatize(self, word):
        # Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

        doc = nlp(word)

        return " ".join([token.lemma_ for token in doc])
        


def cleaning(df: pd.DataFrame):
    # run: python -m spacy download en_core_web_sm
    nlp = spacy.load('en_core_web_sm')

    # Remove missing values if any
    if not df.isnull().sum().empty:
        df = df.dropna().reset_index(drop=True)
        df.isnull().sum()

    # Clean the column "review/text"
    brief_cleaning = (re.sub("[^A-Za-z']+", " ", str(row)).lower() for row in df['description'])
    txt = [clean(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000, n_threads=-1)]

    # Put the results in a DataFrame to remove missing values and duplicates:
    df_clean = pd.DataFrame({'clean': txt})
    df_clean = df_clean.dropna().drop_duplicates()

    df_clean.to_csv('Data/winemagClean.csv')
    df_clean.to_csv('Data/winemagClean2.csv', index=False)

def clean(doc):
    # Lemmatizes and removes stopwords
    # doc needs to be a spacy Doc object
    txt = [token.lemma_ for token in doc if not token.is_stop]
    # Word2Vec uses context words to learn the vector representation of a target word,
    # if a sentence is only one or two words long,
    # the benefit for the training is very small
    if len(txt) > 2:
        return ' '.join(txt)


# Tasks:
    # 
    # Should $ be converted to " dollar" ??
    
