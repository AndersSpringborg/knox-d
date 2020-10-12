
def find_similarities(w2v_model, glove_model, pre_model):
    # Initialize the return variables
    w2v_score_list = list()
    glove_score_list = list()

    # Open the file containing 1000 unique test words
    with open('Data/1000Words.txt', 'r') as infile:
        # Each line contains 1 word and a newline character: '\n'
        for line in infile:
            # Remove the newlines at the end of each line
            word = line.rstrip('\n')

            # Find top 5 most similar words with each model
            w2v_list = w2v_model.wv.most_similar(word, topn=5)
            glove_list = glove_model.most_similar(word, topn=5)
            pre_list = pre_model.most_similar(word, topn=5)

            # Now compare the top 5 most similar words from glove and word2vec with the google result
            w2v_score, glove_score = compare_similarities(w2v_list, glove_list, pre_list)

            # Add the result to the score list for both w2v and glove
            w2v_score_list.append(w2v_score)
            glove_score_list.append(glove_score)

    # Return the sum correct hits for the w2v_score_list and glove_score_list
    return sum(w2v_score_list), sum(glove_score_list)


def compare_similarities(w2v_list, glove_list, spacy_list):
    # Compare the similarities from the Word2Vec list with the Google list
    # w2v_result = sum(element in google_list for element in w2v_list).
    # Compare the similarities from the Word2Vec list with the Google list
    # glove_result = sum(element in google_list for element in glove_list).

    # Other method:
    # Unzip the tuples using zip()
    # This allows for the elements of each tuple to be stored in two separate variables
    # We are only interested in comparing the words, not the vector representations!
    w2v_element1, w2v_element2 = zip(*w2v_list)
    glove_element1, glove_element2 = zip(*glove_list)
    spacy_element1, google_element2 = zip(*spacy_list)

    w2v_result = sum(element in spacy_element1 for element in w2v_element1)
    glove_result = sum(element in spacy_element1 for element in glove_element1)

    return w2v_result, glove_result
