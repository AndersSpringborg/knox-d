from resources.term_frequency import TermFrequency


class TestTermFrequency:
    def setup_method(self):
        self.term_index = TermFrequency()
        self.doc = 'doc1'

    def test_count_a_word_which_is_processed(self):
        term = 'word'
        self.term_index.process(self.doc, term)

        frequency = self.term_index[self.doc][term]

        assert frequency == 1

    def test_second_word_in_sentence_is_processed(self):
        sentence = 'the house'
        second_word = 'house'
        self.term_index.process(self.doc, sentence)

        frequency = self.term_index[self.doc][second_word]

        assert frequency == 1

    def test_count_two_of_the_same_words(self):
        sentence = 'a very very big house'
        word = 'very'
        self.term_index.process(self.doc, sentence)

        frequency = self.term_index[self.doc][word]

        assert frequency == 2

    def test_process_two_sentences_from_different_docs(self):
        word = 'sentence'
        doc_1 = 'doc1'
        doc_2 = 'doc2'

        self.term_index.process(doc_1, word)
        self.term_index.process(doc_2, word)
        doc_from_words = self.term_index[word]

        assert all(doc in doc_from_words
                   for doc in [doc_1, doc_2])

    def test_get_documents_where_a_word_is_found(self):
        term = 'word'
        self.term_index.process(self.doc, term)

        doc_from_words = self.term_index[term]

        assert self.doc in doc_from_words
