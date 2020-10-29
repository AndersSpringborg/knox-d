from typing import List


class Paragraph:
    page: str = ''
    text: str = ''

    def __init__(self, data: dict = None):
        if data:
            self.page = data.get("page", "")
            self.text = data.get("text", "")


class Section:
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
    publisher: str = ''
    published_at: str = ''
    title: str = ''
    sections: List[Section] = []

    def __init__(self, data: dict = None):

        if data:
            self.publisher = data.get("publisher", "")

            self.published_at = data.get("publishedAt", "")

            self.title = data.get("title", "")

            self.sections: List[Section] = []

            if 'sections' in data.keys():
                json_sections = data["sections"].get("items", [])
                for sec in json_sections:
                    self.sections.append(Section(sec['properties']))
