import json, os
from flask import request, make_response, send_from_directory
from werkzeug.utils import secure_filename
from utils.auth_handler import AuthHandler
from config import AppConfig
from utils.text import preprocess, csv_cleaning

from models import db
from models.Text import Text

config = AppConfig()
auth = AuthHandler()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in set(['txt', 'csv'])

# @auth.auth_wrapper
def text():
    req = request.json
    req_text = req['text']

    if isinstance(req_text, list):
        result_text = [ preprocess(text) for text in req_text]
    elif isinstance(req_text, str):
        result_text = preprocess(req_text)
        text = Text(original=result_text['original'], result=result_text['result'])
        db.session.add(text)
        db.session.commit()
    else:
        result_text = None

    result = {
        "success" : True,
        "error"   : None,
        "message" : "Text Cleansing",
        "data"    : result_text
    }
    return make_response(json.dumps(result), 200)

def file():
    if 'file' not in request.files:
        result = {
            "success" : False,
            "error"   : "File Not Found",
            "message" : "No file part in the request",
            "data"    : None
        }
        return json.dumps(result)

    file = request.files['file']
    if file.filename == '':
        result = {
            "success" : False,
            "error"   : "File Not Found",
            "message" : "No file selected for uploading",
            "data"    : None
        }
        return json.dumps(result)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            f = csv_cleaning(file, "Tweet")
            
            result = {
                "success" : False,
                "error"   : None,
                "message" : "File successfully uploaded",
                "data"    : {
                    "file" : f"https://app.xsanjaya.me/api/data/files/{f['filename']}"
                }
            }
            return make_response(json.dumps(result), 200)
       
        except Exception as err:
            result = {
                "success" : False,
                "error"   : str(err),
                "message" : "CSV Cleaning error",
                "data"    : None
            }
            return result
    else:
        result = {
            "success" : False,
            "error"   : "File Not Allowed",
            "message" : "Allowed file types CSV",
            "data"    : []
        }
        return json.dumps(result)

def get_file(file_name):
    return send_from_directory(config.UPLOAD_FOLDER, file_name, as_attachment=True)