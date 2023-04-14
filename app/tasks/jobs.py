
from celery import shared_task
from py7zr import SevenZipFile
from flask import current_app
from zipfile import ZipFile
from tarfile import open
from os import path

from app.database import db
from app.tasks.models import Task

def convert_file(id):
    print(id)
    task = Task.query.get(id)
    if task:
        uploads = path.join(path.dirname(current_app.root_path), current_app.config['UPLOAD_DIR'])

        format = task.new_format.lower()
        filename = task.filename
        processed_filename = f'{task.id}.{format}'

        input_path = path.join(uploads, filename)
        output_path = path.join(uploads, processed_filename) 

        if format == '7z':
            with ZipFile(output_path, mode='w') as f:
                f.write(input_path, arcname=filename)

        if format == 'zip':
            with SevenZipFile(output_path, mode='w') as f:
                f.write(input_path, arcname=filename)

        if format == 'tar.gz':
            with open(output_path, mode='w:gz') as f:
                f.add(input_path, arcname=filename)

        task.status = 'PROCESSED'
        task.processed_filename = processed_filename
        db.session.commit()

@shared_task(ignore_result=False)
def convert_files():
    tasks = Task.query.filter_by(status = 'UPLOADED')
    if tasks:
        for task in tasks:
            try:
                convert_file(task.id)
            except:
                task.status = 'ERROR'
                db.session.commit()
