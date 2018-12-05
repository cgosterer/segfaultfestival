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

class SongForm(FlaskForm):			# used to add a song for a band
	songname = StringField('Song Name', validators=[DataRequired(), Length(min=1, max=50)])		# removed DataRequired()
	bandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max =50)])
	album = StringField('Album Name', validators=[DataRequired(), Length(min=1, max =50)])
	runTime = StringField('Run Time HH:MM:SS (Must be 8 Characters as Shown)', validators=[DataRequired(), Length(min=8, max=8)])
	submit = SubmitField('Create Song')

class UnlikeSongForm(FlaskForm):		# user is already tracked
	usongname = StringField('Song Name', validators=[DataRequired(), Length(min=1, max=50)])
	ubandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max=50)])
	ualbumname = StringField('Album Name', validators=[DataRequired(), Length(min=1, max=50)])
	usubmit = SubmitField('Remove Song')

class UnlikeBandForm(FlaskForm):		# user is already tracked dont need to add user field here
	ubandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max=50)]) # bandname to unlike
	usubmit = SubmitField('Remove Band')

class UserBandForm(FlaskForm):			# Add a band to favorites band List
	bandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max=50)])
	submit = SubmitField('Add Band')

class UserSongForm(FlaskForm):			#  add a band to favorites song list
	songname =StringField('Song Name', validators=[DataRequired(), Length(min=1, max=50)])
	bandname = StringField('Band Name', validators=[DataRequired(), Length(min=1, max=50)])
	album = StringField('Album Name', validators=[DataRequired(), Length(min=1, max=50)])
	submit = SubmitField('Create Favorite')

class DispBandsForm(FlaskForm):
	submit = SubmitField('Show Favorite Bands')

class DispSongsForm(FlaskForm):
	submit = SubmitField('Show Favorite Songs')
