import os
import json
from resources.json_wrapper import Content, Manual


def load_json_file_into_content_object(path: str) -> Content:
    """
    Loads a json file into a Content object.
    """
    if os.stat(path).st_size > 0:
        with open(path, 'r', encoding='utf8') as file:
            data = json.load(file)

        return Content(data['properties']['content']['properties'])

    raise IOError


def load_json(io_stream):
    if io_stream:
        with io_stream as json_file:
            data = json.load(json_file)
        return instantiate_content_object(data)
    raise IOError


def instantiate_content_object(data: dict):
    con = Content(data["properties"]["content"]["properties"])
    return Manual(publisher=con.publisher,
                  published_at=con.published_at,
                  title=con.title)
    # return Content(data["properties"]["content"]["properties"])
