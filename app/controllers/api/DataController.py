import json
from flask import request
from werkzeug.utils import secure_filename

from utils.text import preprocess


def text():
    req = request.json
    req_text = req['text']

    if isinstance(req_text, list):
        result_text = [ preprocess(text) for text in req_text]
    elif isinstance(req_text, str):
        result_text = preprocess(req_text)
    else:
        result_text = None

    result = {
        "success" : True,
        "error"   : None,
        "message" : "Text Cleansing",
        "data"    : result_text
    }

    return json.dumps(result)

def file():
    req      = request.form.to_dict()
    req_file = request.files.to_dict()
    print(req, req_file)

    result = {
        "success" : True,
        "error"   : None,
        "message" : "Text Cleansing",
        "data"    : []
    }

    return json.dumps(result)