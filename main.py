from w2v import *
from testmodule import *
import gensim.models
import spacy


# Create new word2vec spacy_model:
# createw2vmodel()

# Load models:
w2v_model = Word2Vec.load('Models/winemodel')
pre_model = gensim.models.KeyedVectors.load_word2vec_format('Models/GoogleNews-vectors-negative300.bin.gz', binary=True)


# Run test on w2v spacy_model:
test(pre_model)