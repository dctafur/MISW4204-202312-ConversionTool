from flask import request
from flask_restful import Resource
from flask_expects_json import expects_json
from base64 import b64decode

from .jobs import convert_file
from .schemas import convert

class Convert(Resource):

    @expects_json(convert)
    def post(self):
        message = request.json['message']
        id = b64decode(message['data']).decode("utf-8").strip()
        convert_file.delay(int(id))
        print(int(id))
        return '', 204
