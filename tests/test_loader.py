import pytest
from loader.file_loader import load_json_file
import json
from pathlib import Path


class TestLoader:

    def setup_method(self):

        self.json_file_path = Path('../test_data/manual_test_file.json').resolve()

    def test_json_load_returns_dict(self):
        # Arrange

        # Act
        with open(self.json_file_path, 'r', encoding='utf8') as file:
            result = json.load(file)

        # Assert
        assert isinstance(result, dict)

    def test_load_json_file_throws_exception_if_invalid_path(self):
        # Arrange
        invalid_path = 'some invalid path'

        # Act

        # Assert
        with pytest.raises(FileNotFoundError):
            load_json_file(invalid_path)

    def test_load_json_file_throws_exception_if_json_file_is_empty(self):
        # Arrange
        empty_file_path = "../test_data/empty_test_file.json"

        # Act

        # Assert
        with pytest.raises(IOError):
            load_json_file(empty_file_path)

    def test_assign_correct_publisher_to_content(self):
        # Arrange
        expected = {'type': 'string'}

        # Act
        result = load_json_file(self.json_file_path)

        # Assert
        assert result.publisher == expected

    def test_assign_correct_published_at_to_content(self):
        # Arrange
        expected = {'type': 'string'}

        # Act
        result = load_json_file(self.json_file_path)

        # Assert
        assert result.published_at == expected

    def test_assign_correct_title_to_content(self):
        # Arrange
        expected = {'type': 'string'}

        # Act
        result = load_json_file(self.json_file_path)
        print(result.publisher)

        # Assert
        assert result.title == expected

    def test_can_extract_sections_to_content(self):
        # Arrange

        # Act
        result = load_json_file(self.json_file_path)

        # Assert
        assert result.sections is not None

    def test_assign_correct_page_to_section(self):
        # Arrange
        expected = {'type': 'string'}

        # Act
        result = load_json_file(self.json_file_path)

        # Assert
        assert (result.sections[0].page == expected)

    def test_assign_correct_header_to_section(self):
        # Arrange
        expected = {'type': 'string'}

        # Act
        result = load_json_file(self.json_file_path)

        # Assert
        assert (result.sections[0].header == expected)

    def test_assign_correct_page_to_paragraph(self):
        # Arrange
        expected = {'type': 'string'}

        # Act
        result = load_json_file(self.json_file_path)

        # Assert
        assert (result.sections[0].paragraphs[0].page == expected)

    def test_assign_correct_text_to_paragraph(self):
        # Arrange
        expected = {'type': 'string'}

        # Act
        result = load_json_file(self.json_file_path)

        # Assert
        assert (result.sections[0].paragraphs[0].text == expected)
