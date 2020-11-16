import pytest
from io import StringIO
from loader.file_loader import load_json_file_into_content_object, load_json
import json
from pathlib import Path


class TestLoader:

    def setup_method(self):

        self.json_file_path = ""
       
    def test_json_load_returns_dict(self):
        # Arrange
        fake_file = '{}'
        with StringIO(fake_file) as json_file:
            result = json.load(json_file)

        # Assert
        assert isinstance(result, dict)

    def test_load_json_file_throws_exception_if_json_file_is_empty(self):
        # Arrange
        empty_file_path = ''

        # Act

        # Assert
        with pytest.raises(IOError):
            load_json(empty_file_path)

    def test_assign_correct_publisher_to_content(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": {"publisher": "some_publisher"}}}}')
        expected = "some_publisher"

        # Act
        result = load_json(fake_file)

        # Assert
        assert result.publisher == expected

    def test_assign_correct_published_at_to_content(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": {"publishedAt": "23/7"}}}}')
        expected = "23/7"

        # Act
        result = load_json(fake_file)

        # Assert
        assert result.published_at == expected

    def test_assign_correct_title_to_content(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": {"title": "ALPHA1"}}}}')
        expected = "ALPHA1"

        # Act
        result = load_json(fake_file)
        print(result.publisher)

        # Assert
        assert result.title == expected

    def test_can_extract_sections_to_content(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": { "sections": { } }}}}')

        # Act
        result = load_json(fake_file)

        # Assert
        assert result.sections is not None

    def test_assign_correct_page_to_section(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": { "sections": { "items": [ {"properties": {"page": "2"} } ] } }}}}')
        expected = "2"
        # Act
        result = load_json(fake_file)

        # Assert
        assert (result.sections[0].page == expected)

    def test_assign_correct_header_to_section(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": { "sections": { "items": [ {"properties": {"header": "hello"} } ] } }}}}')
        expected = "hello"
        # Act
        result = load_json(fake_file)

        # Assert
        assert (result.sections[0].header == expected)

    def test_assign_correct_page_to_paragraph(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": { "sections": { "items": [ {"properties": { "paragraphs": {"items": [{ "properties": { "page": "3" }} ]}  } } ] } }}}}')
        expected = "3"
        # Act
        result = load_json(fake_file)
        # Assert
        assert (result.sections[0].paragraphs[0].page == expected)

    def test_assign_correct_text_to_paragraph(self):
        # Arrange
        fake_file = StringIO('{"properties": {"content": {"properties": { "sections": { "items": [ {"properties": { "paragraphs": {"items": [{ "properties": { "text": "hello world" }} ]}  } } ] } }}}}')
        expected = "hello world"
        # Act
        result = load_json(fake_file)

        # Assert
        assert (result.sections[0].paragraphs[0].text == expected)
