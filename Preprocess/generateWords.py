import gensim
from gensim.models import Word2Vec

amount_of_words = 0

model = Word2Vec.load('Models/winemodel')
with open('Data/1000Words.txt', 'w') as f:
    for word in model.wv.vocab:
        if amount_of_words < 1000:
            if len(word) > 3:
                amount_of_words += 1
                f.write(word+'\n')
