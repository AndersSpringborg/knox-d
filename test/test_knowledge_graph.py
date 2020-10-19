import pytest
from Knowledge_Graph.knowledgegraph import KnowledgeGraph
from tokencontainer import Token
class Test_Knowledge_Graph:
    def test_subject_object_pairing(self):
        # Arrange
        self.result = ()
        sentence = []
        expected = ('martin', 'computerspil')

        # Act
        token1 = Token('martin', 'subj')
        token2 = Token('computerspil', 'obj')
        sentence.append(token1)
        sentence.append(token2)
        kg = KnowledgeGraph(sentence)
        result = kg.get_subject_and_object_pair(sentence)
        #Assert
        assert expected == result