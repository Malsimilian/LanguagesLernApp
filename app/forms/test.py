from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class QuestionForm(FlaskForm):
    question = StringField('Вопрос', validators=[DataRequired()])
    answer1 = StringField('1 вариант ответа', validators=[DataRequired()])
    answer2 = StringField('2 вариант ответа', validators=[DataRequired()])
    answer3 = StringField('3 вариант ответа', validators=[DataRequired()])
    answer4 = StringField('4 вариант ответа', validators=[DataRequired()])
    correct_answer = StringField('Верный варинат', validators=[DataRequired()])
    submit = SubmitField('Submit')



