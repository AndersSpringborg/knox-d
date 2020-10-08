from preprocess.bigrams import bigram_detection
from preprocess.cleaner import cleaning
import pandas as pd
import multiprocessing
from gensim.models import Word2Vec

def createw2vmodel():
    # Predefines
    INPUT_FILE = 'Data/winemagClean.csv'

    # Read the file
    df = pd.read_csv(INPUT_FILE)

    # Remove missing values if any -- OUTCOMMENT THIS FUNCTION CALL IF THE FILE IS NOT CLEANED
    # cleaning(df)

    # Create bigrams
    sentences = bigram_detection(df)

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