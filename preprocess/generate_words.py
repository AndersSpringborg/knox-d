from gensim.models import Word2Vec

AMOUNT_OF_WORDS = 0

model = Word2Vec.load('Models/winemodel')
with open('Data/1000Words.txt', 'w') as f:
    for word in model.wv.vocab:
        if AMOUNT_OF_WORDS < 1000:
            if len(word) > 3:
                AMOUNT_OF_WORDS += 1
                f.write(word+'\n')
