import json
import os.path
from io import StringIO

from loader.file_loader import load_json
from resources import knox_triples
from resources.json_wrapper import Manual
from word_embedding.token import Token
from resources.knowledgegraph_info_container import KnowledgeGraphInfo
from word_embedding.dependency import Dependency

from mi_graph.knowledge_graph import KnowledgeGraph


class TestKnowledgeGraph:

    def setup_method(self):
        self.kg = KnowledgeGraph()

    def teardown_method(self):
        self.kg.knowledge_graph_triples = []
        # Erase file after tests
        if os.path.isfile("test_files/testfile.csv"):
            os.remove("test_files/testfile.csv")

    # Reafactor to send to database, instead of saving to csv file
    def xtest_creates_csv_file_in_correct_folder(self):
        # Arrange
        sentences = []
        manual = Manual()
        kg_info = KnowledgeGraphInfo(sentences, manual)

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

        manual = Manual()

        kg_info = KnowledgeGraphInfo(sentence, manual)

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

        manual = Manual()

        kg_info = KnowledgeGraphInfo(sentences, manual)

        # Act
        self.kg.generate_triples(kg_info)
        result = self.kg.knowledge_graph_triples

        # Assert
        assert isinstance(result, list)
        assert len(result) == 4

    # 0 metadata
    # 1 title
    def test_generate_triple_for_publisher(self):
        # Arrange
        data = {
            "published_by": "some_publisher",
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
            "published_by": "some_publisher",
            "title": "manual123",
            "published_at": "2020-11-13"
        }

        self.__setup_data_in_kg(data)
        result = self.kg.knowledge_graph_triples[1]

        expected = knox_triples.PublishedAtTriple("manual123", "2020-11-13")

        # Assert
        assert result.published_at == expected.published_at
        assert result.manual_uri == expected.manual_uri

    def test_generate_triple_for_title(self):
        data = {
            "published_by": "grundfos",
            "title": "manual1337",
            "published_at": "2020-11-14"
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
            "sections": [{
                "header": "some_header"
            }]
        }

        self.__setup_data_in_kg(data)

        assert self.kg.knowledge_graph_triples[2].section_title == "some_header"

    def test_generate_triples_for_multiple_sections(self):
        data = {
            "sections": [
                {
                    "header": "some_header"
                },
                {
                    "header": "some_header2"
                }
            ]
        }

        self.__setup_data_in_kg(data)
        result = self.kg.knowledge_graph_triples

        assert result[0].section_title == "some_header"
        assert result[1].section_title == "some_header2"

    def test_generate_triple_for_header_and_page(self):
        data = {
            "sections": [{
                "page": "some_page",
                "header": "some_header"
            }]
        }

        self.__setup_data_in_kg(data)

    def __setup_data_in_kg(self, data):
        new_data = {'content': data}
        manual = load_json(StringIO(json.dumps(new_data)))
        sentences = []
        self.kg.generate_triples(KnowledgeGraphInfo(sentences, manual))
