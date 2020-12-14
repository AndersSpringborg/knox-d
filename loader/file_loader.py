import json
from resources.json_wrapper import Content, Manual


def load_json(io_stream):
    if io_stream:
        with io_stream as json_file:
            data = json.load(json_file)
        return instantiate_content_object(data)
    raise IOError


def instantiate_content_object(data: dict):
    con = Content(data["content"])
    return Manual(publisher=con.published_by,
                  published_at=con.published_at,
                  title=con.title,
                  sections=con.sections)
