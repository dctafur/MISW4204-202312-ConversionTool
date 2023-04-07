from flask_restful import Resource
from flask_jwt_extended import jwt_required


class ReadFile(Resource):

    @jwt_required()
    def get(self, file_name):
        return {"file_name": file_name}
