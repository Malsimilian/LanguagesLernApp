# import sqlalchemy
# from .db_session import SqlAlchemyBase
# from flask_login import UserMixin
# from sqlalchemy import orm
#
# class Test(SqlAlchemyBase, UserMixin):
#     __tablename__ = 'tests'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer,
#                            primary_key=True, autoincrement=True)
#     questions = orm.relationship('Questions', backref='test')
