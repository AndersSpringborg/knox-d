from gensim.models.phrases import Phrases, Phraser
import pandas as pd


def bigram_detection(df: pd.DataFrame):
    """
        makes bigrams in  a column named clean, in a Panda dataframe

    :param df: pd.Dataframe
    :return: word_tokens []
    """
    word_tokens = [row.split() for row in df['clean']]

    phrases = Phrases(word_tokens, min_count=30, progress_per=10000)

    bigram = Phraser(phrases)

    return bigram[word_tokens]
