import os
import sys

from Resources.JsonWrapper import Content
import json

def load_json_file(path: str) -> Content:
    try:
        if os.stat(path).st_size > 0:
            with open(path, 'r', encoding='utf8') as file:
                data = json.load(file)
            return Content(data['properties']['content']['properties'])
        else:
            raise IOError
    except FileNotFoundError as e:
        raise e

