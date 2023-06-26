from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired, Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed


class AskForm(FlaskForm):
    name = StringField('Name:',validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(),Email()])
    subject = StringField('Subject:',validators=[DataRequired()])
    message = StringField('Message:',validators=[DataRequired()])
    submit = SubmitField('Send message')
