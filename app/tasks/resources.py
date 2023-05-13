from json import load
from os import environ
from time import gmtime
from calendar import timegm
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import get_current_user, jwt_required
from google.cloud import storage, pubsub_v1
from google.auth import jwt

from app.database import db
from app.tasks.models import Task, TaskSchema


class TaskCrud(Resource):

    @jwt_required()
    def get(self, id=None):
        user = get_current_user()

        if not id:
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

        if (task.user_id != user.id):
            return {'message': 'You don\'t have permissions to access this task'}, 403

        task_schema = TaskSchema()
        return task_schema.dump(task), 200

    @jwt_required()
    def post(self):
        if 'filename' not in request.files:
            return {'message': 'No file part'}, 400

        file = request.files['filename']
        if file.filename == '':
            return {'message': 'No selected file'}, 400

        new_format = request.form['newFormat']
        allowed_formats = ['7Z', 'ZIP', 'TAR.GZ']
        if not new_format in allowed_formats:
            return {'message': f'Allowed formats are: {", ".join(allowed_formats)}'}, 400

        time_stamp = timegm(gmtime())
        custom_name = f'{time_stamp}.{file.filename}'
        file.filename = custom_name

        gcs = storage.Client.from_service_account_json(current_app.config['CREDENTIALS'])
        bucket = gcs.get_bucket(environ.get('BUCKET_NAME'))
        blob = bucket.blob(file.filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)

        user = get_current_user()
        task = Task(filename=custom_name, new_format=new_format, user_id=user.id)
        db.session.add(task)
        db.session.commit()

        task_schema = TaskSchema()
        task_response = task_schema.dump(task)

        service_account_info = load(open('credentials-pubsub.json'))
        audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
        credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=audience)
        publisher = pubsub_v1.PublisherClient(credentials=credentials)
        topic_path = publisher.topic_path(environ.get('PROJECT_ID'), environ.get('CONVERT_TOPIC_ID'))
        publisher.publish(topic_path, str(task.id).encode("utf-8"))

        return task_response, 201

    @jwt_required()
    def delete(self, id):
        user = get_current_user()
        task = Task.query.get_or_404(id)

        if (task.user_id != user.id):
            return {'message': 'You don\'t have permissions to delete this task'}, 403

        if task.status != 'PROCESSED':
            return {'message': 'The task is still being processed'}, 400

        gcs = storage.Client.from_service_account_json(current_app.config['CREDENTIALS'])
        bucket = gcs.get_bucket(environ.get('BUCKET_NAME'))
        blob = bucket.blob(task.filename)
        processed_blob = bucket.blob(task.processed_filename)
        blob.delete()
        processed_blob.delete()

        db.session.delete(task)
        db.session.commit()
        return '', 204
