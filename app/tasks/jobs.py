
from os import environ
from io import BytesIO
from flask import current_app
from celery import shared_task
from py7zr import SevenZipFile
from zipfile import ZipFile
from tarfile import TarFile, TarInfo
from google.cloud import storage

from app.database import db
from app.tasks.models import Task


@shared_task(ignore_result=False)
def convert_files():
    tasks = Task.query.filter_by(status='ERROR')
    if tasks:
        for task in tasks:
            try:
                format = task.new_format.lower()
                filename = task.filename
                processed_filename = f'{task.id}.{format}'

                gcs = storage.Client.from_service_account_json(current_app.config['CREDENTIALS'])
                bucket = gcs.get_bucket(environ.get('BUCKET_NAME'))

                input_blob = bucket.blob(filename)
                input_file = input_blob.download_as_string()
                output_file = BytesIO()

                if format == '7z':
                    with SevenZipFile(file=output_file, mode='w') as f:
                        f.writestr(data=input_file, arcname=filename)

                if format == 'zip':
                    with ZipFile(file=output_file, mode='w') as f:
                        f.writestr(data=input_file, zinfo_or_arcname=filename)

                if format == 'tar.gz':
                    with TarFile.open(fileobj=output_file, mode='w:gz') as f:
                        info = TarInfo(filename)
                        info.size = len(input_file)
                        f.addfile(fileobj=BytesIO(input_file), tarinfo=info)

                output_blob = bucket.blob(processed_filename)
                output_blob.upload_from_string(output_file.getvalue())

                task.status = 'PROCESSED'
                task.processed_filename = processed_filename
                db.session.commit()
            except:
                task.status = 'ERROR'
                db.session.commit()
