import pytest
import pandas as pd
import os.path
from pandas._testing import assert_frame_equal
from resources.json_wrapper import Content
from word_embedding.token import Token
from resources.knowledgegraph_info_container import KnowledgeGraphInfo
from word_embedding.dependency import Dependency

from mi_graph.knowledgegraph import KnowledgeGraph, Triple


class TestKnowledgeGraph:

    database_filepath = 'knowledgegraphtestfile.csv'

    def setup_method(self):
        self.kg = KnowledgeGraph(self.database_filepath)

    def teardown_method(self):
        # Erase file after tests
        os.remove(self.database_filepath)

    def test_creates_csv_file_in_correct_folder(self):
        # Arrange
        sentences = []
        content = Content()
        kg_info = KnowledgeGraphInfo(sentences, content)

        # Act
        self.kg.generate_triples(kg_info)
        file_exists = os.path.isfile(self.database_filepath)

        # Assert
        assert file_exists

    def test_validate_analyse_single_sentence(self):
        # Arrange
        sentence = [[Token('martin', dep=Dependency.nsubj),
                     Token('likes', dep=Dependency.root),
                     Token('computerspil', dep=Dependency.obj)]]

        content = Content()

        kg_info = KnowledgeGraphInfo(sentence, content)

        triple = Triple('martin', 'likes', 'computerspil')

        expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})

        # Act
        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        # Assert
        assert_frame_equal(result, expected)

    def test_validate_analyse_multiple_sentences(self):

        # Arrange
        sentences = [[Token('Martin', dep=Dependency.nsubj),
                      Token('likes', dep=Dependency.root),
                      Token('computerspil', dep=Dependency.obj)],
                     [Token('Kasper', dep=Dependency.nsubj),
                      Token('loves', dep=Dependency.root),
                      Token('computerspil', dep=Dependency.obj)],
                     [Token('Martin', dep=Dependency.nsubj),
                      Token('enjoys', dep=Dependency.root),
                      Token('apples', dep=Dependency.obj)],
                     [Token('Lars', dep=Dependency.nsubj),
                      Token('hates', dep=Dependency.root),
                      Token('computerspil', dep=Dependency.obj)]]

        content = Content()

        kg_info = KnowledgeGraphInfo(sentences, content)

        triple1 = Triple('Martin', 'likes', 'computerspil')
        triple2 = Triple('Kasper', 'loves', 'computerspil')
        triple3 = Triple('Martin', 'enjoys', 'apples')
        triple4 = Triple('Lars', 'hates', 'computerspil')

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
        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        # Assert
        assert_frame_equal(result, expected)

    def test_generate_triple_for_publisher(self):
        sentences = []

        triple = Triple('manual', 'publishedBy', 'some_publisher')

        expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})

        data = {
            "publisher": "some_publisher"
        }

        content = Content(data)

        kg_info = KnowledgeGraphInfo(sentences, content)

        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)

    def test_generate_triple_for_published_at(self):
        triple = Triple('manual', 'publishedAt', 'some_date')

        expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})

        data = {
            "publishedAt": "some_date"
        }

        content = Content(data)
        sentences = []
        kg_info = KnowledgeGraphInfo(sentences, content)

        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)

    def test_generate_triple_for_title(self):
        triple = Triple('manual', 'describes', 'some_title')

        expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})

        data = {
            "title": "some_title"
        }

        content = Content(data)

        sentences = []
        kg_info = KnowledgeGraphInfo(sentences, content)

        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)

    def test_generate_triple_for_section(self):
        triple = Triple('manual', 'contains', 'some_header')

        expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})

        data = {
            "sections": {
                "items": [
                    {
                        "properties": {
                            "header": "some_header"
                        }

                    }
                ]
            }
        }

        content = Content(data)
        sentences = []
        kg_info = KnowledgeGraphInfo(sentences, content)

        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)

    def test_generate_triples_for_multiple_sections(self):
        triple = Triple('manual', 'contains', 'some_header')
        triple2 = Triple('manual', 'contains', 'some_header2')

        expected = pd.DataFrame(columns=['subject', 'relation', 'object'])

        expected = expected.append(
            pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]}),
            ignore_index=True)

        expected = expected.append(
            pd.DataFrame({'subject': [triple2.subj], 'relation': [triple2.rel], 'object': [triple2.obj]}),
            ignore_index=True)

        data = {
            "sections": {
                "items": [
                    {
                        "properties": {
                            "header": "some_header"
                        }

                    },
                    {
                        "properties": {
                            "header": "some_header2"
                        }

                    }
                ]
            }
        }

        content = Content(data)

        sentences = []
        kg_info = KnowledgeGraphInfo(sentences, content)

        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)

    def test_generate_triple_for_header_and_page(self):
        triple2 = Triple('some_header', 'isAt', 'some_page')
        triple = Triple('manual', 'contains', 'some_header')

        expected = pd.DataFrame(columns=['subject', 'relation', 'object'])

        expected = expected.append(pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]}),
                                   ignore_index=True)

        expected = expected.append(pd.DataFrame({'subject': [triple2.subj], 'relation': [triple2.rel], 'object': [triple2.obj]}),
                                   ignore_index=True)

        data = {
            "sections": {
                "items": [
                    {
                        "properties": {
                            "page": "some_page",
                            "header": "some_header"
                        }

                    }
                ]
            }
        }

        content = Content(data)

        sentences = []
        kg_info = KnowledgeGraphInfo(sentences, content)

        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)

    def test_generate_triple_for_multiple_header_and_page_pairs(self):
        triple = Triple('manual', 'contains', 'some_header')
        triple2 = Triple('manual', 'contains', 'some_header2')
        triple3 = Triple('some_header', 'isAt', 'some_page')
        triple4 = Triple('some_header2', 'isAt', 'some_page2')

        expected = pd.DataFrame(columns=['subject', 'relation', 'object'])

        expected = expected.append(
            pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]}),
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

        data = {
            "sections": {
                "items": [
                    {
                        "properties": {
                            "page": "some_page",
                            "header": "some_header"
                        }

                    },
                    {
                        "properties": {
                            "page": "some_page2",
                            "header": "some_header2"
                        }

                    }
                ]
            }
        }

        content = Content(data)

        sentences = []
        kg_info = KnowledgeGraphInfo(sentences, content)

        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)

    def test_generate_triples_if_only_title_and_publisher(self):
        triple = Triple('manual', 'publishedBy', 'Grundfos')
        triple2 = Triple('manual', 'describes', "ALPHA1")

        expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})
        expected = expected.append(
            pd.DataFrame({'subject': [triple2.subj], 'relation': [triple2.rel], 'object': [triple2.obj]}),
            ignore_index=True)

        dict = {
            "publisher": "Grundfos",
            "title": "ALPHA1"
        }

        content = Content(dict)
        sentences = []
        kg_info = KnowledgeGraphInfo(sentences, content)
        self.kg.generate_triples(kg_info)
        result = pd.read_csv(self.database_filepath)

        assert_frame_equal(result, expected)
