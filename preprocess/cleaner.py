import spacy
import re
import time
import pandas as pd

# run: python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')


def cleaning(df: pd.DataFrame):
    # Remove missing values if any
    if not df.isnull().sum().empty:
        df = df.dropna().reset_index(drop=True)
        df.isnull().sum()

    # Clean the column "review/text"
    brief_cleaning = (re.sub("[^A-Za-z']+", ' ', str(row)).lower() for row in df['description'])
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


