import sqlalchemy
import sqlalchemy.orm as orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase  # Предполагается, что SqlAlchemyBase - это базовый класс SQLAlchemy

class Question(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String)
    answer1 = sqlalchemy.Column(sqlalchemy.String)
    answer2 = sqlalchemy.Column(sqlalchemy.String)
    answer3 = sqlalchemy.Column(sqlalchemy.String)
    answer4 = sqlalchemy.Column(sqlalchemy.String)
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('lessons.id'))
    lesson = orm.relationship('Lesson', backref='questions_lesson')
