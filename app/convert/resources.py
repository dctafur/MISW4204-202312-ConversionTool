from flask import request
from flask_restful import Resource

from .jobs import convert_file


class Convert(Resource):

    def post(self):
        id = request.json['id']
        convert_file.delay(id)
        return '', 204
