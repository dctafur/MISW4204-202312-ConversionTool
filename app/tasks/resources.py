from flask import request
from flask_restful import Resource
from flask_expects_json import expects_json
from flask_jwt_extended import get_current_user, jwt_required

from app.database import db
from app.tasks.models import Task, TaskSchema
from app.tasks.jobs import convert_file
from app.tasks.schemas import create_task


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
    @expects_json(create_task)
    def post(self):
        user = get_current_user()
        file_name = request.json['fileName']
        new_format = request.json['newFormat']

        allowed_formats = ['7Z', 'ZIP', 'TAR.GZ']
        if not new_format in allowed_formats:
            return {'message': f'Allowed formats are: {", ".join(allowed_formats)}'}, 400

        task = Task(file_name=file_name, new_format=new_format, user_id=user.id)
        db.session.add(task)
        db.session.commit()

        convert_file.delay(task.id)

        task_schema = TaskSchema()
        return task_schema.dump(task), 201

    @jwt_required()
    def delete(self, id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return '', 204
