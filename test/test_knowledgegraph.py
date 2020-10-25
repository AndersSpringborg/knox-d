import pytest
import pandas as pd
import os.path
from pandas._testing import assert_frame_equal

from Resources.TokenContainer import Token

from Knowledge_Graph.knowledgegraph import KnowledgeGraph, Triple


class TestKnowledgeGraph:

    database_filepath = 'knowledgegraphtestfile.csv'

    def setup_method(self):
        self.kg = KnowledgeGraph(self.database_filepath)

    def teardown_method(self):
        # Erase file after tests
        os.remove(self.database_filepath)

    def test_creates_csv_file_in_correct_folder(self):
        # Arrange
        sentence = [[Token('martin', 'subj'),
                     Token('likes', 'adj'),
                     Token('computerspil', 'obj')]]

        # Act
        self.kg.update(sentence)
        file_exists = os.path.isfile(self.database_filepath)

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

        # Assert
        assert_frame_equal(result, expected)

    def test_validate_file_content_containing_multiple_rows(self):

        # Arrange
        sentence = [[Token('martin', 'subj'),
                     Token('likes', 'adj'),
                     Token('computerspil', 'obj')],
                    [Token('kasper', 'subj'),
                     Token('loves', 'adj'),
                     Token('computerspil', 'obj')],
                    [Token('martin', 'subj'),
                     Token('enjoys', 'adj'),
                     Token('apples', 'obj')],
                    [Token('lars', 'subj'),
                     Token('hates', 'adj'),
                     Token('computerspil', 'obj')]]

        triple1 = Triple('martin', 'likes', 'computerspil')
        triple2 = Triple('kasper', 'loves', 'computerspil')
        triple3 = Triple('martin', 'enjoys', 'apples')
        triple4 = Triple('lars', 'hates', 'computerspil')

        expected = pd.DataFrame(columns=['subject', 'relation', 'object'])

        expected = expected.append(
            pd.DataFrame({'subject': [triple1.subj], 'relation': [triple1.rel], 'object': [triple1.obj]}),
            ignore_index=True)

        expected = expected.append(
            pd.DataFrame({'subject': [triple2.subj], 'relation': [triple2.rel], 'object': [triple2.obj]}),
            ignore_index=True)

        expected = expected.append(
            pd.DataFrame({'subject': [triple3.subj], 'relation': [triple3.rel], 'object': [triple3.obj]}),
            ignore_index=True)

        expected = expected.append(
            pd.DataFrame({'subject': [triple4.subj], 'relation': [triple4.rel], 'object': [triple4.obj]}),
            ignore_index=True)

        # Act
        self.kg.update(sentence)
        result = pd.read_csv('knowledgegraphtestfile.csv')
        self.kg.show_graph()

        # Assert
        assert_frame_equal(result, expected)
