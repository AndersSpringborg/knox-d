from typing import List


class Manual:
    """
    The data structure for the manual.
    This is the only one that should be used in the rest of the project

    """

    def __init__(self, title='', publisher='', published_at='', sections=''):
        self.title: str = title
        self.published_by: str = publisher
        self.published_at: str = published_at
        self.sections: [] = sections


class Paragraph:
    """
    Data-structure for the information stored under
    each paragraph in the "paragraph" array in the json file
    """
    page: str = ''
    text: str = ''

    def __init__(self, data: dict = None):
        if data:
            self.page = data.get("page", "")
            self.text = data.get("text", "")


class Section:
    """
    Data-structure for the information stored under
    each section in the "sections" array in the json file
    """

    def __init__(self, data: dict = None):
        if data:
            self.page = data.get("page", "")
            self.header = data.get("header", "")

            if 'paragraphs' in data.keys():
                json_paragraph = data.get("paragraphs", "")
                self.paragraph = Paragraph(json_paragraph)


class Content:
    """
    Data-structure for the information stored under "content" in the json file
    """
    publisher: str = ''
    published_at: str = ''
    title: str = ''
    sections: List[Section] = []

    def __init__(self, data: dict = None):

        if data:
            self.publisher = data.get("publisher")

            if publish_date := data.get("publishedAt"):
                self.published_at = publish_date

            self.title = data.get("title")

            self.sections: List[Section] = []

            if 'sections' in data.keys():
                json_sections = recursive_parse_section(data)
                for section in json_sections:
                    self.sections.append(Section(section))


def recursive_parse_section(data: {}) -> []:
    if "sections" in data.keys():
        array_of_sections = data.get('sections')
        for section in array_of_sections:
            new_flat_array_of_section = recursive_parse_section(section)

            if "sections" in section.keys():
                del section['sections']

            array_of_sections = array_of_sections + new_flat_array_of_section

        return array_of_sections

    return []
