# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class NoteForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(max=150)])
    content = TextAreaField('Содержание', validators=[DataRequired(), Length(max=2000)])
    submit = SubmitField('Сохранить')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(max=80)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class DeleteForm(FlaskForm):
    submit = SubmitField('Удалить')
