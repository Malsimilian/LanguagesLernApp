import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm


class Lesson(SqlAlchemyBase, UserMixin):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    text_material = sqlalchemy.Column(sqlalchemy.String)
    video_material = sqlalchemy.Column(sqlalchemy.String)
    # tests = orm.relationship('Tests', backref='lesson')
    course_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('courses.id'))
    course = orm.relationship('Course', backref='lessons_course')
