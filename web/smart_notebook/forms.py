from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, PasswordField, BooleanField

from smart_notebook.models import User


# -------------------------------------------------Login/Logout---------------------------------------------------------


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# ----------------------------------------------------SignUp------------------------------------------------------------


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_number = StringField('Phone ', validators=[DataRequired(), Length(min=10, max=16)])
    postal_code = StringField('Postal Code ', validators=[DataRequired(), Length(max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There is an existing account associated with this email.')

    def validate_phone_number(self, phone_number):
        if not phone_number.data.isnumeric():
            raise ValidationError('Phone number must be numbers only.')


# ------------------------------------------------Forgot Pass-----------------------------------------------------------


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account associated with the email.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


# -------------------------------------------------Notes----------------------------------------------------------------


class NoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateNoteForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


# --------------------------------------------------Account-------------------------------------------------------------


class AccountUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone_number = StringField('Phone ', validators=[DataRequired(), Length(min=10, max=16)])
    postal_code = StringField('Postal Code ', validators=[DataRequired(), Length(max=6)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('There is an existing account associated with this email.')

    def validate_phone_number(self, phone_number):
        if not phone_number.data.isnumeric():
            raise ValidationError('Phone number must be numbers only.')


# -------------------------------------------------Search---------------------------------------------------------------

class SearchForm(FlaskForm):
    search_content = StringField('Search Content', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Search')


# ------------------------------------------------Arithmetic------------------------------------------------------------

class FibonacciForm(FlaskForm):
    start = IntegerField('Start', validators=[DataRequired()])
    range = IntegerField('Range', validators=[DataRequired()])
    submit = SubmitField('Submit')


class QuadraticForm(FlaskForm):
    a = IntegerField('Value A', validators=[DataRequired()])
    b = IntegerField('Value B', validators=[DataRequired()])
    c = IntegerField('Value C', validators=[DataRequired()])
    submit = SubmitField('Submit')
