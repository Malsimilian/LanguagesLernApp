from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    name = StringField('Название курса', default=None)
    language_choices = [('', 'Любой'), ('english', 'English'), ('french', 'French'), ('spanish', 'Spanish')]
    language = SelectField('Choose a language', choices=language_choices, default=('', 'Любой'))
    difficulty_choices = [('', 'Любая'), ('a1', 'a1'), ('a2', 'a2'), ('b1', 'b1'), ('b2', 'b2'), ('c1', 'c1'), ('c2', 'c2')]
    difficulty = SelectField('Choose a dificulty', choices=difficulty_choices, default=('', 'Любая'))
    submit = SubmitField('Найти курсы')