from os import path
from flask import current_app, send_from_directory
from flask_restful import Resource
from flask_jwt_extended import get_current_user, jwt_required

from app.tasks.models import Task

class ReadFile(Resource):

    @jwt_required()
    def get(self, filename):
        user = get_current_user()
        task = Task.query.filter_by(processed_filename=filename).one_or_none()

        if (not task or task.user_id != user.id):
            return {'message': 'You don\'t have permissions to read this file'}, 403

        uploads = path.join(path.dirname(current_app.root_path), current_app.config['UPLOAD_DIR'])
        return send_from_directory(uploads, filename, as_attachment=True)
