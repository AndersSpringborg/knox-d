from preprocess import *

sentences = CleanSentence('TestData')  # Directory with the test data

model = Word2Vec(size=300,
                 window=10,
                 min_count=3)
model.build_vocab(sentences)
model.train(sentences=sentences, total_examples=model.corpus_count, epochs=model.epochs)
model.save('tmp/w2vmodel')  # Save the model for later use