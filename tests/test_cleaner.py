import pytest
from preprocess.cleaner_imp import CleanerImp


class TestCleaner:

    def setup_method(self):
        self.cleaner = CleanerImp()

    def test_init_cleaner(self):
        assert self.cleaner is not None

    def test_can_create_bigram(self):
        sentence = "I like to eat ice cream in new york."
        expected = "I like to eat ice_cream in new_york."

        result = self.cleaner.bigrams(sentence)

        assert result == expected


    def test_can_create_trigram(self):
        sentence = "Cloud computing is benefiting major manufacturing companies"
        expected = "Cloud_computing is benefiting major_manufacturing_companies"

        result = self.cleaner.bigrams(sentence)

        assert result == expected

    def test_cleaner_makes_words_to_lowercase(self):
        text = "Hi My Name Is Torben"

        lower_case_text = self.cleaner.to_lower(text)

        expected_text = "hi my name is torben"
        assert expected_text == lower_case_text

    def test_cleaner_removes_single_special_character(self):
        text = "I have five $ in my wallet"

        cleaned_text = self.cleaner.remove_special_characters(text)

        expexted_text = "I have five  in my wallet"
        assert expexted_text == cleaned_text

    def test_cleaner_removes_many_special_characters(self):
        text = 'My "#¤&%/)(name! \'is@ torben?¨^`'
        expexted_text = "My name is torben"

        cleaned_text = self.cleaner.remove_special_characters(text)

        assert expexted_text == cleaned_text

    def test_cleaner_removes_many_special_characters_keep_punct(self):
        text = 'My "#¤&%/)(name! \'is@ torben.?¨^`'
        expexted_text = "My name is torben."

        cleaned_text = self.cleaner.remove_special_characters(text)

        assert expexted_text == cleaned_text

    def test_cleaner_should_textify_single_digit(self):
        text = "I have 5 dollars in my pocket"
        expected_text = "I have five dollars in my pocket"

        cleaned_text = self.cleaner.numbers_to_text(text)

        assert expected_text == cleaned_text

    def test_cleaner_should_textity_long_number(self):
        text = "34567"
        expected_text = "three four five six seven"

        cleaned_text = self.cleaner.numbers_to_text(text)

        assert expected_text == cleaned_text

    def test_cleaner_should_textity_double_digits(self):
        text = "54"
        expected_text = "five four"

        cleaned_text = self.cleaner.numbers_to_text(text)

        assert expected_text == cleaned_text

    def test_remove_duplicates_in_string_list(self):
        text_list = ['Hej mit navn er Torben.',
                     'Hej mit navn er Solvej.',
                     'Hej mit navn er Torben.']
        expected_text = ['Hej mit navn er Torben.',
                         'Hej mit navn er Solvej.']

        duplicates_removed = self.cleaner.remove_duplicates(text_list)

        assert set(expected_text) == set(duplicates_removed)

    def test_lemmatize_walking_to_walk(self):
        sentence = "walking"

        lemma_word = self.cleaner.lemmatize(sentence)

        assert lemma_word == 'walk'

    def test_lemmatize_feet_to_foot(self):
        sentence = "feet"

        lemma_word = self.cleaner.lemmatize(sentence)

        assert lemma_word == 'foot'

    def test_lemmatize_multiple_words(self):
        sentence = "walking feet"

        lemmatized = self.cleaner.lemmatize(sentence)

        assert lemmatized == "walk foot"

    def xtest_valuta_gets_lemmatised_to_text(self):
        sentence = "Many $"

        lemmatized = self.cleaner.lemmatize(sentence)

        assert lemmatized == "many dollar"

# Test ideas
