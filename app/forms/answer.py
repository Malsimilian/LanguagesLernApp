from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


class TestForm(FlaskForm):
    answer_choices = [('1', 'A'), ('2', 'B'), ('3', 'C'), ('4', 'D')]
    answer = SelectField(choices=answer_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')
