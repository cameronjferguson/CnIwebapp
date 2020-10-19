from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from corkandink.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min = 2, max = 50)])
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                                validators=[DataRequired(), Length(min=2, max = 60)])
    confirm_password = PasswordField('Confirm Password', 
                                        validators=[DataRequired(), Length(min=2, max = 60), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email address already has an account. Please Log in or use a different email')


class LoginForm(FlaskForm):
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                                validators=[DataRequired(), Length(min=2, max = 60)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min = 2, max = 50)])
    email = StringField('Email', 
                            validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email address already has an account. Please Log in or use a different email')


class WineForm(FlaskForm):
    title = StringField('Name', validators=[DataRequired()])
    #brand = StringField('Brand')
    #region = StringField('Region')
    #grape = StringField('Grape')
    #country = StringField('Country')
    #year = IntegerField('Vintage')
    #wine_type = SelectField('Wine Type', choices=['red', 'white', 'rose', 'sparkling', 'fruit', 'other'])
    #location = StringField('Where did you drink the wine?')
    #price = DecimalField('Price of wine')
    #purch_loc = StringField('Where did you buy the wine?')
    #purch_url = StringField('Purchase url')
    #rating = SelectField('Rating out of 5', ['1', '2', '3', '4', '5'])
    content = TextAreaField('Tasting notes', validators=[DataRequired()])
    submit = SubmitField('Add Wine')