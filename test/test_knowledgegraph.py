import pytest

from tokencontainer import Token

from Knowledge_Graph.knowledgegraph import KnowledgeGraph


class TestKnowledgeGraph:

    def setup_method(self):
        self.kg = KnowledgeGraph()

        # Erase file content before testing
        with open('knowledgegraph.txt', 'w'): pass

    def test_process_sentence(self):

        # Arrange
        sentence = [[Token('martin', 'subj'),
                     Token('likes', 'adj'),
                     Token('computerspil', 'obj')]]

        expected = 'martin --> likes --> computerspil\n'

        # Act
        self.kg.update(sentence)
        result = self.kg.get_knowledge_graph()

        # Assert
        assert result == expected
