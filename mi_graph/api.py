import json
from io import StringIO

from flask import Flask, Response, request

from loader.file_loader import load_json
from mi_graph import pipeline

app = Flask(__name__)


def start_api():
    app.run(debug=True)


@app.route('/api/manuals', methods=['POST'])
def process_manual():
    manual = create_manual_from_request(request.json)
    try:
        pipeline.run(manual)
    except Exception as error:  # pylint: disable=W0703
        return Response(response=str(error),
                        status=400,
                        content_type='application/json')

    return Response(response=json.dumps({"success": True}),
                    status=201,
                    content_type='application/json')


def create_manual_from_request(json_data):
    json_dump = json.dumps(json_data)
    data_as_io_stream = StringIO(json_dump)
    manual = load_json(data_as_io_stream)
    return manual
