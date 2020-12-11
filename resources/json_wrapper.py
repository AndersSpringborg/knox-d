from datetime import datetime
from typing import List


class Manual:
    def __init__(self, title='', publisher='', published_at='', sections=''):
        self.title: str = title
        self.published_by: str = publisher
        self.published_at: datetime = published_at
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
    page: str = ''
    header: str = ''
    paragraphs: List[Paragraph] = []

    def __init__(self, data: dict = None):
        if data:
            self.page = data.get("page", "")
            self.header = data.get("header", "")

            if 'paragraphs' in data.keys():
                self.paragraphs: List[Paragraph] = []
                json_paragraphs = data['paragraphs'].get("items", [])
                for para in json_paragraphs:
                    self.paragraphs.append(Paragraph(para['properties']))


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
                self.published_at = datetime.strptime(publish_date, '%Y-%d-%m')

            self.title = data.get("title", "")

            self.sections: List[Section] = []

            if 'sections' in data.keys():
                json_sections = data["sections"].get("items", [])
                for sec in json_sections:
                    section = sec['properties']
                    self.sections.append(Section(section))


def recursive_parse_section(data: {}) -> []:
    if "sections" in data.keys():
        section = data['sections']
        all_sections = [section] + recursive_parse_section(section)

        if "sections" in all_sections[0].keys():
            del all_sections[0]['sections']

        return all_sections
    else:
        return []
