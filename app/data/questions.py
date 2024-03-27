# import sqlalchemy
# from .db_session import SqlAlchemyBase
# from flask_login import UserMixin
# from sqlalchemy import orm
#
# class Quest(SqlAlchemyBase, UserMixin):
#     __tablename__ = 'quests'
#
#     id = sqlalchemy.Column(sqlalchemy.Integer,
#                            primary_key=True, autoincrement=True)
#     quest = sqlalchemy.Column(sqlalchemy.String)
#     answer = sqlalchemy.Column(sqlalchemy.Integer)
