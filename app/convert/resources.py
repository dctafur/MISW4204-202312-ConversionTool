from flask_restful import Resource

from .jobs import convert_file


class Convert(Resource):

    def get(self, id):
        convert_file.delay(id)
        return '', 204
