import pytest
import pandas as pd
import os.path
from pandas._testing import assert_frame_equal

from rdf_parser import rdf_helper
from resources import knox_triples
from resources.json_wrapper import Content
from word_embedding.token import Token
from resources.knowledgegraph_info_container import KnowledgeGraphInfo
from word_embedding.dependency import Dependency

from knowledge_graph.knowledge_graph import KnowledgeGraph


class TestKnowledgeGraph:

    def setup_method(self):
        self.kg = KnowledgeGraph()

    def teardown_method(self):
        self.kg.knowledge_graph_triples = []
        # Erase file after tests
        if os.path.isfile("test_files/testfile.csv"):
            os.remove("test_files/testfile.csv")

    def test_creates_csv_file_in_correct_folder(self):
        # Arrange
        sentences = []
        content = Content()
        kg_info = KnowledgeGraphInfo(sentences, content)

        # Act
        self.kg.generate_triples(kg_info)
        self.kg.save_to_csv("test_files/testfile.csv")
        file_exists = os.path.isfile("test_files/testfile.csv")

        # Assert
        assert file_exists

    def test_validate_analyse_single_sentence(self):
        # Arrange
        sentence = [[Token('Pump', dep=Dependency.nsubj),
                     Token('develop', dep=Dependency.root),
                     Token('well', dep=Dependency.obj)]]

        content = Content()

        kg_info = KnowledgeGraphInfo(sentence, content)

        # Act
        self.kg.generate_triples(kg_info)
        result = self.kg.knowledge_graph_triples

        # Assert
        assert isinstance(result[0], knox_triples.SentenceTriple)
        assert len(result) == 1

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

        # Act
        self.kg.generate_triples(kg_info)
        result = self.kg.knowledge_graph_triples

        # Assert
        assert isinstance(result, list)
        assert len(result) == 4

    def test_generate_triple_for_publisher(self):
        # Arrange
        data = {
            "publisher": "some_publisher",
            "title": "manual123"
        }
        self.__setup_data_in_kg(data)

        result = self.kg.knowledge_graph_triples[0]

        expected = knox_triples.PublishTriple('manual123', 'some_publisher')

        # Assert
        assert result.publisher == expected.publisher
        assert result.manual_uri == expected.manual_uri

    def test_generate_triple_for_published_at(self):
        data = {
            "publisher": "some_publisher",
            "title": "manual123",
            "publishedAt": "2020-11-13"
        }

        self.__setup_data_in_kg(data)
        result = self.kg.knowledge_graph_triples[1]

        expected = knox_triples.PublishedAtTriple("manual123", "2020-11-13")

        # Assert
        assert result.published_at == expected.published_at
        assert result.manual_uri == expected.manual_uri

    def test_generate_triple_for_title(self):
        data = {
            "publisher": "grundfos",
            "title": "manual1337",
            "publishedAt": "2020-11-14"
        }

        self.__setup_data_in_kg(data)
        result = self.kg.knowledge_graph_triples[3]

        expected = knox_triples.TitleTriple("manual1337")

        # Assert
        assert result.title == expected.title
        assert result.manual_uri == expected.manual_uri

    def test_generate_triple_for_section(self):
        data = {
            "title": "manual123",
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

        self.__setup_data_in_kg(data)

        assert self.kg.knowledge_graph_triples[2].section_title == "some_header"

    def test_generate_triples_for_multiple_sections(self):
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

        self.__setup_data_in_kg(data)
        result = self.kg.knowledge_graph_triples

        assert result[0].section_title == "some_header"
        assert result[1].section_title == "some_header2"

    def test_generate_triple_for_header_and_page(self):
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

        self.__setup_data_in_kg(data)

    # def test_generate_triple_for_multiple_header_and_page_pairs(self):
    #     triple = Triple('manual', 'contains', 'some_header')
    #     triple2 = Triple('manual', 'contains', 'some_header2')
    #     triple3 = Triple('some_header', 'isAt', 'some_page')
    #     triple4 = Triple('some_header2', 'isAt', 'some_page2')
    #
    #     expected = pd.DataFrame(columns=['subject', 'relation', 'object'])
    #
    #     expected = expected.append(
    #         pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]}),
    #         ignore_index=True)
    #
    #     expected = expected.append(
    #         pd.DataFrame({'subject': [triple2.subj], 'relation': [triple2.rel], 'object': [triple2.obj]}),
    #         ignore_index=True)
    #
    #     expected = expected.append(
    #         pd.DataFrame({'subject': [triple3.subj], 'relation': [triple3.rel], 'object': [triple3.obj]}),
    #         ignore_index=True)
    #
    #     expected = expected.append(
    #         pd.DataFrame({'subject': [triple4.subj], 'relation': [triple4.rel], 'object': [triple4.obj]}),
    #         ignore_index=True)
    #
    #     data = {
    #         "sections": {
    #             "items": [
    #                 {
    #                     "properties": {
    #                         "page": "some_page",
    #                         "header": "some_header"
    #                     }
    #
    #                 },
    #                 {
    #                     "properties": {
    #                         "page": "some_page2",
    #                         "header": "some_header2"
    #                     }
    #
    #                 }
    #             ]
    #         }
    #     }
    #
    #     content = Content(data)
    #
    #     sentences = []
    #     kg_info = KnowledgeGraphInfo(sentences, content)
    #
    #     self.kg.generate_triples(kg_info)
    #     result = pd.read_csv(self.database_filepath)
    #
    #     assert_frame_equal(result, expected)
    #
    # def test_generate_triples_if_only_title_and_publisher(self):
    #     triple = Triple('manual', 'publishedBy', 'Grundfos')
    #     triple2 = Triple('manual', 'describes', "ALPHA1")
    #
    #     expected = pd.DataFrame({'subject': [triple.subj], 'relation': [triple.rel], 'object': [triple.obj]})
    #     expected = expected.append(
    #         pd.DataFrame({'subject': [triple2.subj], 'relation': [triple2.rel], 'object': [triple2.obj]}),
    #         ignore_index=True)
    #
    #     dict = {
    #         "publisher": "Grundfos",
    #         "title": "ALPHA1"
    #     }
    #
    #     content = Content(dict)
    #     sentences = []
    #     kg_info = KnowledgeGraphInfo(sentences, content)
    #     self.kg.generate_triples(kg_info)
    #     result = pd.read_csv(self.database_filepath)
    #
    #     assert_frame_equal(result, expected)

    def __setup_data_in_kg(self, data):
        content = Content(data)
        sentences = []
        self.kg.generate_triples(KnowledgeGraphInfo(sentences, content))
