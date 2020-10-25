from typing import List

# For additional information on the usage of dict:
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/


class Paragraph:
    page: str
    text: str

    def __init__(self, data: dict):
        self.page = data.get("page", "")
        self.text = data.get("text", "")


class Section:
    page: str
    header: str
    paragraphs: List[Paragraph]

    def __init__(self, data: dict):
        self.page = data.get("page", "")
        self.header = data.get("header", "")
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
        self.publisher = data.get("publisher", "")
        self.publishedAt = data.get("publishedAt", "")
        self.title = data.get("title", "")
        self.sections: List[Section] = []
        json_sections = data["sections"].get("items", [])
        for sec in json_sections:
            self.sections.append(Section(sec['properties']))
