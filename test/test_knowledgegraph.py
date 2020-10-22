import pytest
import pandas as pd
import os.path
from pandas._testing import assert_frame_equal

from tokencontainer import Token

from Knowledge_Graph.knowledgegraph import KnowledgeGraph, Triple


class TestKnowledgeGraph:

    def setup_method(self):
        self.kg = KnowledgeGraph()

        # Erase file content before testing
        with open('knowledgegraph.txt', 'w'): pass

    def test_creates_csv_file_in_correct_folder(self):
        # Arrange
        filepath = 'knowledgegraphtestfile.csv'
        sentence = [[Token('martin', 'subj'),
                     Token('likes', 'adj'),
                     Token('computerspil', 'obj')]]

        # Act
        self.kg.update(sentence)
        file_exists = os.path.isfile(filepath)

        # Assert
        assert file_exists

    def test_validate_file_content(self):

        # Arrange
        sentence = [[Token('martin', 'subj'),
                     Token('likes', 'adj'),
                     Token('computerspil', 'obj')]]

        triple = Triple('martin', 'likes', 'computerspil')

        expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})

        # Act
        self.kg.update(sentence)
        result = pd.read_csv('knowledgegraphtestfile.csv')
        print(result)
        print(expected)

        # Assert
        assert_frame_equal(result, expected)

