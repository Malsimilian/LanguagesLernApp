import sqlalchemy
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy import orm


user_to_favorite_courses_table = sqlalchemy.Table(
    'user_to_favorite_courses',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('courses', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('courses.id'))
)

class Course(SqlAlchemyBase, UserMixin):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    language = sqlalchemy.Column(sqlalchemy.String)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    difficulty = sqlalchemy.Column(sqlalchemy.String)
    lessons = orm.relationship('Lesson', backref='course_lessons')
    author = orm.relationship('User', backref='author_courses')
