
from celery import shared_task
from py7zr import SevenZipFile
from zipfile import ZipFile
from tarfile import open

from app.database import db
from app.tasks.models import Task


@shared_task(ignore_result=True)
def convert_file(id):
    task = Task.query.get(id)
    if task:
        # TODO: Get upload dir from app config
        upload_dir = 'data'

        format = task.new_format.lower()
        filename = task.filename

        input_path = f'{upload_dir}/{filename}'
        output_path = f'{upload_dir}/{task.id}.{format}'

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
        task.processed_filename = output_path
        db.session.commit()
