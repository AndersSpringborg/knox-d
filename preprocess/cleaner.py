import abc
from abc import ABC


class Cleaner(ABC):
    """
    A class that have the responsibility to clean strings.
    It handles preprocessing
    """
    @abc.abstractmethod
    def bigrams(self, sentence: str) -> str:
        """
        returns list of bigram, from a string
        a bigram is a concatenation of a noun_chunk e.g: "New York" --> "New_York"



        :param sentence: str
        :return: sentence: str
                """

    @abc.abstractmethod
    def to_lower(self, words) -> str:
        """
        makes a string to lowercase characters

        :param words:
        :return: the input string to lower
        """

    @abc.abstractmethod
    def remove_special_characters(self, txt: str) -> str:
        """
        Removes special characters from a string

        :param txt:
        :return:
        """

    @abc.abstractmethod
    def lemmatize(self, words: str) -> str:
        """
        lemmatizes all words in a string full of words

        :param words:
        :return: words lemmatized, same format as string
        """

    def remove_duplicates(self, str_list: [str]) -> [str]:
        """


        :param str_list: a list of strings, where you want duplicates removed
        :return: a list of strings, with the duplicates removed
        """
