import pytest
from Loader.FileLoader import load_json_file
from Resources.JsonWrapper import Content, Section, Paragraph

class TestLoader:

    def setup_method(self):
        pass

    def test_assign_correct_publisher_to_content(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'

        # Act
        result = load_json_file(json_file_path)

        # Assert
        assert result.publisher == {'type': 'string'}

    def test_assign_correct_publishedAt_to_content(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'

        # Act
        result = load_json_file(json_file_path)
        print(result.publisher)

        # Assert
        assert result.publishedAt == {'type': 'string'}

    def test_assign_correct_title_to_content(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'


        # Act
        result = load_json_file(json_file_path)
        print(result.publisher)

        # Assert
        assert result.title == {'type': 'string'}

    def test_can_extract_sections_to_content(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'

        # Act
        result = load_json_file(json_file_path)
        print(result.publisher)

        # Assert
        assert result.sections is not None




    def test_assign_correct_page_to_section(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'

        # Act
        result = load_json_file(json_file_path)

        # Assert
        assert (result.sections[0].page == {'type': 'string'})


    def test_assign_correct_header_to_section(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'

        # Act
        result = load_json_file(json_file_path)

        # Assert
        assert (result.sections[0].header == {'type': 'string'})


    def test_assign_correct_page_to_paragraph(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'

        # Act
        result = load_json_file(json_file_path)

        # Assert
        assert (result.sections[0].paragraphs[0].page == {'type': 'string'})


    def test_assign_correct_text_to_paragraph(self):
        # Arrange
        json_file_path = '../TestData/manual_test_file.json'

        # Act
        result = load_json_file(json_file_path)

        # Assert
        assert (result.sections[0].paragraphs[0].text == {'type': 'string'})