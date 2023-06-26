from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired, Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from project.models import User

################################################################################
#################################Login Form#####################################
################################################################################
class LoginForm(FlaskForm):
    email = StringField(' ', validators=[DataRequired(),Email()])
    password = PasswordField(' ',validators=[DataRequired()])
    submit = SubmitField('Submit')
################################################################################
#############################Registration Form##################################
################################################################################
class RegistrationForm(FlaskForm):
    email = StringField('',validators=[DataRequired(),Email()])
    username = StringField('',validators=[DataRequired()])
    password = PasswordField('',validators=[DataRequired(),EqualTo('pass_confirm')])
    pass_confirm = PasswordField('',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Your email has been registered already!')
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('Your username has been registered already!')
################################################################################
###############################Update User Form#################################
################################################################################
class UpdateUserForm(FlaskForm):
    email = StringField('Email: ',validators=[DataRequired(),Email()])
    username = StringField('Username: ',validators=[DataRequired()])
    picture =  FileField('Update profile picture: ',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Your username has been registered already!')
################################################################################
###################################Ask Form#####################################
################################################################################
class AskForm(FlaskForm):
    name = StringField('Name:',validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(),Email()])
    message = StringField('Message:',validators=[DataRequired()])
    submit = SubmitField('Send message')
################################################################################
#############################Forgot Password Form###############################
################################################################################
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')
################################################################################
###########################Change Password Form#################################
################################################################################
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
