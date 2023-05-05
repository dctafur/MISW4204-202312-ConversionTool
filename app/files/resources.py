from os import environ
from io import BytesIO
from flask import current_app, send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from google.cloud import storage


class ReadFile(Resource):

    @jwt_required()
    def get(self, filename):
        gcs = storage.Client.from_service_account_json(current_app.config['CREDENTIALS'])
        bucket = gcs.get_bucket(environ.get('BUCKET_NAME'))
        blob = bucket.blob(filename)
        file = blob.download_as_string()
        return send_file(BytesIO(file), download_name=filename, as_attachment=True)
