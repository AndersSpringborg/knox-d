from typing import List

# For additional information on the usage of dict:
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/


class Paragraph:
    page: str
    text: str

    def __init__(self, data: dict):
        if 'page' in data.keys():
            self.page = data.get("page", "")

        if 'text' in data.keys():
            self.text = data.get("text", "")


class Section:
    page: str
    header: str
    paragraphs: List[Paragraph]

    def __init__(self, data: dict):
        if 'page' in data.keys():
            self.page = data.get("page", "")

        if 'header' in data.keys():
            self.header = data.get("header", "")

        if 'paragraphs' in data.keys():
            self.paragraphs: List[Paragraph] = []
            json_paragraphs = data['paragraphs'].get("items", [])
            for para in json_paragraphs:
                self.paragraphs.append(Paragraph(para['properties']))


class Content:
    publisher: str
    publishedAt: str
    title: str
    sections: List[Section]

    def __init__(self, data: dict):

        if 'publisher' in data.keys():
            self.publisher = data.get("publisher", "")

        if 'publishedAt' in data.keys():
            self.publishedAt = data.get("publishedAt", "")

        if 'title' in data.keys():
            self.title = data.get("title", "")

        if 'sections' in data.keys():
            self.sections: List[Section] = []
            json_sections = data["sections"].get("items", [])
            for sec in json_sections:
                self.sections.append(Section(sec['properties']))
