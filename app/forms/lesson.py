from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired


class LessonForm(FlaskForm):
    name = StringField('Название урока', validators=[DataRequired()])
    video = StringField('Введите ссылку на видео материал')
    text = StringField('Введите текстовый материал')
    submit = SubmitField('Создать курс')