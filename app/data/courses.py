import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm


class Courses(SqlAlchemyBase, UserMixin):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    language = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    lessons = orm.relationship('Lessons', backref='course')
