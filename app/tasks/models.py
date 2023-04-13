from sqlalchemy.sql import func

from app.database import db, ma


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(1000), nullable=False)
    new_format = db.Column(db.String(1000), nullable=False)
    status = db.Column(db.String(255), server_default='UPLOADED')
    created_at = db.Column(db.DateTime, server_default=func.now())
    processed_filename = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task

    id = ma.auto_field()
    filename = ma.auto_field()
    processed_filename = ma.auto_field()
    new_format = ma.auto_field()
    status = ma.auto_field()
    created_at = ma.auto_field()
