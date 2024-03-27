from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class CourseForm(FlaskForm):
    name = StringField('Название курса', validators=[DataRequired()])
    language_choices = [('english', 'English'), ('french', 'French'), ('spanish', 'Spanish')]
    language = SelectField('Choose a language', choices=language_choices)
    submit = SubmitField('Создать курс')