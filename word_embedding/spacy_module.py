import spacy
from gensim.models.keyedvectors import WordEmbeddingsKeyedVectors

def createspacymodel():
    # The spacy model consists of the pre-trained model: 'en_core_web_lg'
    # The purpose of this function is to reformat the pre-trained model so gensim can read it
    nlp = spacy.load('en_core_web_lg')

    words = []
    vectors = []
    # extract words and their vectors
    for key, vector in nlp.vocab.vectors.items():
        words.append(nlp.vocab.strings[key])
        vectors.append(vector)

    # Create instance of the class
    keyedVectors = WordEmbeddingsKeyedVectors(nlp.vocab.vectors_length)
    # Add words and vectors
    keyedVectors.add(words, vectors)
    keyedVectors.wv.save('Models/premodel')




