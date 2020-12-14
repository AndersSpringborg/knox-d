from datetime import datetime

import pytest
from io import StringIO
from loader.file_loader import load_json_file_into_content_object, load_json
import json
from pathlib import Path

from resources.json_wrapper import recursive_parse_section


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
        fake_file = StringIO('{"content": {"publisher": "some_publisher"}}')
        expected = "some_publisher"

        result = load_json(fake_file)

        assert result.published_by == expected

    def test_assign_correct_published_at_to_content(self):
        # Arrange
        fake_file = StringIO('{"content": {"publishedAt": "2020-23-07"}}')
        expected = datetime(2020, day=23, month=7)

        # Act
        result = load_json(fake_file)

        # Assert
        assert result.published_at == expected

    def test_assign_correct_title_to_content(self):
        fake_file = StringIO('{"content": {"title": "ALPHA1"}}')
        expected = "ALPHA1"

        result = load_json(fake_file)

        assert result.title == expected

    def test_can_extract_sections_to_content(self):
        # Arrange
        fake_file = StringIO('{"content": { "sections": [{ }] }}')

        # Act
        result = load_json(fake_file)

        # Assert
        assert result.sections is not None

    def test_assign_correct_page_to_section(self):
        fake_file = StringIO('{"content":{ "sections": [{"page": "2", "header": "info"}] }}')
        expected_page = "2"

        result = load_json(fake_file)
        first_section = 0
        assert (result.sections[first_section].page == expected_page)

    def test_assign_correct_header_to_section(self):
        # Arrange
        fake_file = StringIO('{"content":{ "sections": [{"header": "hello"}] }}')
        expected = "hello"
        # Act
        result = load_json(fake_file)

        # Assert
        assert (result.sections[0].header == expected)

    def test_assign_correct_page_to_paragraph(self):
        # Arrange
        fake_file = StringIO('{"content": { "sections": [{ "paragraphs": {"page": "3"} }] }}')
        expected = "3"
        # Act
        result = load_json(fake_file)
        # Assert
        assert (result.sections[0].paragraph.page == expected)

    def test_assign_correct_text_to_paragraph(self):
        # Arrange
        fake_file = StringIO('{"content": {"sections": [{"paragraphs": {"text": "hello world"}}]}}')
        expected = "hello world"
        # Act
        result = load_json(fake_file)

        # Assert
        assert (result.sections[0].paragraph.text == expected)

    def test_parse_two_recursive_sections(self):
        content = StringIO('{"content": { "sections": [{"sections": [{"info": "test_2"}],"info": "test_1"}]}}')

        full_manual = load_json(content)

        assert len(full_manual.sections) == 2


def make_grundfos_schema(mid: str):
    start = '{"properties": {"properties": {'
    end = '}}}}'

    return StringIO(start + mid + end)


class TestRecursiveParser:
    def test_recurse_section_base_case(self):
        data = {"sections": [{"info": "test"}]}

        list_of_sections = recursive_parse_section(data)

        assert len(list_of_sections) == 1
        assert list_of_sections[0]['info'] == "test"

    def test_recurse_section_two_sections(self):
        data = {
            "sections": [{
                "sections": [{
                    "info": "test_2"}],
                "info": "test_1"}]
        }

        list_of_sections = recursive_parse_section(data)

        assert list_of_sections[0]['info'] == "test_1"
        assert list_of_sections[1]['info'] == "test_2"

    def test_recurse_section_three_sections(self):
        data = {
            "sections": [{
                "sections": [{
                    "sections": [{
                        "info": "test_3"}],
                    "info": "test_2"}],
                "info": "test_1"}]
        }

        list_of_sections = recursive_parse_section(data)

        assert list_of_sections[0]['info'] == "test_1"
        assert list_of_sections[1]['info'] == "test_2"
        assert list_of_sections[2]['info'] == "test_3"

    def test_first_section_do_not_have_section(self):
        data = {
            "sections": [{
                "sections": [{
                    "info": "test_2"}],
                "info": "test_1"}]
        }

        list_of_sections = recursive_parse_section(data)
        print(list_of_sections)
        assert "sections" not in list_of_sections[0].keys()
