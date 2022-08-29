import json
from flask import request
from werkzeug.utils import secure_filename

def text():
    req = request.json
    req_text = req['text']

    result = {
        "success" : True,
        "error"   : None,
        "message" : "Text Cleansing",
        "data"    : [ text for text in req_text ]
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