from typing import List

import pytest
import pandas as pd
import os.path
from pandas._testing import assert_frame_equal
from Resources.JsonWrapper import Content
from Resources.TokenContainer import Token
from Resources.KnowledgeGraphInfoContainer import KnowledgeGraphInfo

from Knowledge_Graph.knowledgegraph import KnowledgeGraph, Triple


class TestKnowledgeGraph:

    database_filepath = 'knowledgegraphtestfile.csv'

    def setup_method(self):
        dictionary = {
            "publisher": "Grundfos",
            "publishedAt": "23/7",
            "title": "ALPHA1",
            "sections": {
                "items": [
                    {
                        "properties": {
                            "page": "3",
                            "header": "General Information",
                            "paragraphs": {
                                "items": [
                                    {
                                        "properties": {
                                            "page": "3",
                                            "text": "The pump is used for Solar panels"
                                        }
                                    }
                                ]
                            }
                        }

                    },
                    {
                        "properties": {
                            "page": "8",
                            "header": "Starting up the product",
                            "paragraphs": {
                                "items": [
                                    {
                                        "properties": {
                                            "page": "8",
                                            "text": "The pump must be turned on"
                                        }
                                    }
                                ]
                            }
                        }

                    }
                ]
            }
        }
        sentences = [[Token('Martin', 'subj'),
                     Token('likes', 'ROOT'),
                     Token('computerspil', 'obj')],
                    [Token('Kasper', 'subj'),
                     Token('loves', 'ROOT'),
                     Token('computerspil', 'obj')],
                    [Token('Martin', 'subj'),
                     Token('enjoys', 'ROOT'),
                     Token('apples', 'obj')],
                    [Token('Lars', 'subj'),
                     Token('hates', 'ROOT'),
                     Token('computerspil', 'obj')]]

        self.kg_info = KnowledgeGraphInfo(sentences, dictionary)

        self.kg = KnowledgeGraph(self.database_filepath)

    def teardown_method(self):
        # Erase file after tests
        os.remove(self.database_filepath)

    def test_creates_csv_file_in_correct_folder(self):
        # Arrange
        sentences = []
        dictionary = {}
        content = Content(dictionary)
        kg_info = KnowledgeGraphInfo(sentences, content)

        # Act
        self.kg.generate_triples(kg_info)
        file_exists = os.path.isfile(self.database_filepath)

        # Assert
        assert file_exists

    def test_validate_analyse_single_sentence(self):
        # Arrange
        sentence = [[Token('martin', 'subj'),
                     Token('likes', 'ROOT'),
                     Token('computerspil', 'obj')]]

        dictionary = {}
        content = Content(dictionary)

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
        sentence = [[Token('martin', 'subj'),
                     Token('likes', 'ROOT'),
                     Token('computerspil', 'obj')],
                    [Token('kasper', 'subj'),
                     Token('loves', 'ROOT'),
                     Token('computerspil', 'obj')],
                    [Token('martin', 'subj'),
                     Token('enjoys', 'ROOT'),
                     Token('apples', 'obj')],
                    [Token('lars', 'subj'),
                     Token('hates', 'ROOT'),
                     Token('computerspil', 'obj')]]

        dictionary = {}
        content = Content(dictionary)

        kg_info = KnowledgeGraphInfo(sentence, content)

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