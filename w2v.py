from gensim.models import Phrases
from gensim.models.phrases import Phraser

from Preprocess.bigrams import bigramDetection
from Preprocess.converter import convertToCsv
from Preprocess.cleaner import cleaning
import pandas as pd
import time
import re
import spacy
import multiprocessing
from gensim.models import Word2Vec

def createw2vmodel():
    # Predefines
    INPUT_FILE = 'Data/winemagClean.csv'

    # Read the file
    df = pd.read_csv(INPUT_FILE)

    # Remove missing values if any
    #cleaning(INPUT_FILE)

    #Create bigrams
    sentences = bigramDetection(df)


    # Train the model
    cores = multiprocessing.cpu_count() # Count the number of cores in a computer
    model = Word2Vec(min_count=2,
                         window=10,
                         size=50,
                         sample=6e-5,
                         alpha=0.03,
                         min_alpha=0.0007,
                         negative=20,
                         workers=cores-1)

    model.build_vocab(sentences, progress_per=10000)
    model.train(sentences, total_examples=model.corpus_count, epochs=30, report_delay=1)
    model.save('Models/winemodel')