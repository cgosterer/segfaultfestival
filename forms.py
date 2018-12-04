from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=40)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign UP')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=40)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class ModRegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=40)])
        email = StringField('Email', validators=[DataRequired(), Email()])
	bandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max = 50)])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Create Mod')

class SongForm(FlaskForm):
        songname = StringField('Song Name', validators=[DataRequired(), Length(min=1, max=50)])
        bandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max =50)])
	album = StringField('Album Name', validators=[DataRequired(), Length(min=1, max =50)])
	runTime = StringField('Run Time HH:MM:SS (Must be 8 Characters as Shown)', validators=[Length(min=8, max =8)])
        submit = SubmitField('Create Song')

class UserSongForm(FlaskForm):
	songname =StringField('Song Name', validators=[DataRequired(), Length(min=1, max=50)]) 
	bandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max=50)])
	album = StringField('Album Name', validators=[DataRequired(), Length(min=1, max=50)])
	submit = SubmitField('Create Favorite')
