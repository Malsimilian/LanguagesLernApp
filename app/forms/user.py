from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    language_choices = [('english', 'English'), ('french', 'French'), ('spanish', 'Spanish')]
    language = SelectField('Choose a language', choices=language_choices)
    submit = SubmitField('Зарегистрироваться')