import logging
import os
import uuid

from flask import Flask, g, jsonify, make_response, request
from flask_cors import CORS
from flask_mysqldb import MySQL

from utility.error import ThrowError
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(filename='record.log',
                    level=logging.DEBUG,
                     format='%(asctime)s | %(levelname)s | %(lineno)d | \n %(message)-20s')

app = Flask(__name__)
CORS(app)

#register blueprints
from api.data_processing_api import data_processing_api
app.register_blueprint(data_processing_api, url_prefix='/api')

def init_db(app):
    db = MySQL(app)
    db.init_app(app)
    return db


db = init_db(app)

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        response = make_response('success', 200)
        response.headers['Access-Control-Allow-Headers'] = '*'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Content-Type'] = '*'
        return response
    else:
        request_id = str(uuid.uuid4())
        g.request_id = request_id

@app.errorhandler(ThrowError)
def handle_throw_error(error):
    response = jsonify({
        "message": str(error),
        "error_code": error.status_code
    })
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT', 5011))