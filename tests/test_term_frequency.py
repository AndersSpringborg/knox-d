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
        doc_from_words = self.term_index.terms[word]

        assert all(doc in doc_from_words
                   for doc in [doc_1, doc_2])

    def test_get_documents_where_a_word_is_found(self):
        word = 'word'
        self.term_index.process(self.doc, word)

        doc_from_words = self.term_index.terms[word]

        assert self.doc in doc_from_words

    def test_count_all_words_in_doc(self):
        five_words = "lorem ipsum dolor sit amet"
        doc = 'doc1'
        self.term_index.process(doc, five_words)

        length = self.term_index[doc].length

        assert length == len(five_words.split(' '))

    def test_count_vocab_in_document(self):
        two_different_words = "lorem lorem ipsum"
        doc = 'doc1'
        self.term_index.process(doc, two_different_words)

        vocab = self.term_index[doc].vocab

        assert vocab == 2

    def test_title_appear_in_corpus(self):
        corpus = "D42 is a pump"
        doc = "D42"
        self.term_index.process(doc, corpus)

        word_document = self.term_index.terms["D42"]

        assert doc in word_document

    def test_doc_do_not_appear_twice_lookup_word(self):
        corpus = "the the"
        doc = "D42"
        self.term_index.process(doc, corpus)

        word_documents = self.term_index.terms["the"]

        assert len(word_documents) == 1

