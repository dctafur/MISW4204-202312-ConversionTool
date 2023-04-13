from os import path
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import get_current_user, jwt_required
from werkzeug.utils import secure_filename

from app.database import db
from app.tasks.models import Task, TaskSchema


class TaskCrud(Resource):

    @jwt_required()
    def get(self, id=None):
        if not id:
            user = get_current_user()
            args = request.args.to_dict()

            sort = 'id' if args.get('sort') is None else args.get('sort')
            order = 'asc' if args.get('order') is None else args.get('order')
            page = 1 if args.get('page') is None else int(args.get('page'))
            limit = 10 if args.get('limit') is None else int(args.get('limit'))

            order_by = getattr(getattr(Task, sort), order)()
            page = Task.query.order_by(order_by).filter_by(user_id=user.id).paginate(page=page, per_page=limit)

            task_schema = TaskSchema()
            meta = {'page': page.page, 'total': page.total}
            return {'items': task_schema.dump(page.items, many=True), 'meta': meta}, 200

        task = Task.query.get_or_404(id)
        task_schema = TaskSchema()
        return task_schema.dump(task), 200

    @jwt_required()
    def post(self):
        if 'filename' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['filename']
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        filename = secure_filename(file.filename)
        uploads = path.join(path.dirname(current_app.root_path), current_app.config['UPLOAD_DIR'])
        file.save(path.join(uploads, filename))

        user = get_current_user()
        new_format = request.form['newFormat']

        allowed_formats = ['7Z', 'ZIP', 'TAR.GZ']
        if not new_format in allowed_formats:
            return {'message': f'Allowed formats are: {", ".join(allowed_formats)}'}, 400

        task = Task(filename=filename, new_format=new_format, user_id=user.id)
        db.session.add(task)
        db.session.commit()

        task_schema = TaskSchema()
        return task_schema.dump(task), 201

    @jwt_required()
    def delete(self, id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return '', 204
