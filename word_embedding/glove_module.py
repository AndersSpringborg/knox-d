from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import get_tmpfile


def createglovemodel():
    glove_file = 'GloveSetup/vectors.txt'
    tmp_file = get_tmpfile('test_w2v.txt')

    _ = glove2word2vec(glove_file, tmp_file)
    model = KeyedVectors.load_word2vec_format(tmp_file)

    model.save('Models/glovemodel')