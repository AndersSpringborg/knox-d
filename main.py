import os
import subprocess

from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import get_tmpfile

from WordEmbeddings.word2vec_module import createw2vmodel
from WordEmbeddings.spacy_module import createspacymodel
from WordEmbeddings.glove_module import createglovemodel
from Preprocess.bigrams import bigram_detection
from Preprocess.cleaner import cleaning
from quality_analysis.test_module import find_similarities
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import pandas as pd


# Create new models:
#createw2vmodel()
#createspacymodel()
#createglovemodel()


# Load models:
w2v_model = Word2Vec.load('Models/winemodel')

#glove_file = 'GloveSetup/vectors.txt'
#tmp_file = get_tmpfile('test_w2v.txt')
#_ = glove2word2vec(glove_file, tmp_file)
#glove_model = KeyedVectors.load_word2vec_format(tmp_file)

# Load the pre-trained model as KeyedVectors rather than a Word2Vec model, since it is simply a metrice of words and
# their vector representations rather than a complete word2vec model!
# pre_model = KeyedVectors.load('Models/premodel')

model = w2v_model.wv

print(model.word_vec('sweet'))

# Run test on most similar results

#w2v_score, glove_score = findsimilarities(w2v_model, glove_model, google_model)
#print('--- WHICH MODEL IS BETTER?? google model ---')
#enunmarator = (869 * 5)
#print('w2v score:   ', w2v_score, " pct: ", w2v_score/enunmarator )
#print('glove score: ', glove_score, " pct: ", glove_score/enunmarator)


