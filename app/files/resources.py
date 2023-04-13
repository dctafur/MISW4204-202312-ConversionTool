from os import path
from flask import current_app, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class ReadFile(Resource):

    @jwt_required()
    def get(self, filename):
        uploads = path.join(path.dirname(current_app.root_path), current_app.config['UPLOAD_DIR'])
        return send_from_directory(uploads, filename, as_attachment=True)
