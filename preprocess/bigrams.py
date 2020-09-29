from gensim.models.phrases import Phrases, Phraser

def bigramDetection(df):
    sent = [row.split() for row in df['clean']]

    phrases = Phrases(sent, min_count=30, progress_per=10000)

    bigram = Phraser(phrases)

    return bigram[sent]
