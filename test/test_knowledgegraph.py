import pytest

from tokencontainer import Token

from Knowledge_Graph.knowledgegraph import KnowledgeGraph

class TestKnowledgeGraph:

    def setup_method(self):
        list = []
        self.kg = KnowledgeGraph(list)

    def test_get_subject_and_object_pair(self):
        # Arrange
        sentence = [Token('martin', 'subj'),
                    Token('likes', 'verb'),
                    Token('computerspil', 'obj')]

        expected = ('martin', 'computerspil')

        # Act
        result = self.kg.get_subject_and_object_pair(sentence)

        # Assert
        assert expected == result
