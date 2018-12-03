import mysql.connector
import random
import time
from hashlib import sha256 as userHash
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, ModRegistrationForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_table import Table, Col
#from flask_bcrypt import Bcrypt
from mysql.connector.cursor import MySQLCursorPrepared
from accountAccess import checkExists, checkPassword, createAccount
#import flask_whooshalchemy as wa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbtest4020:Pp0gHfo-~149@den1.mysql1.gear.host/dbtest4020'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
#app.config['WHOOSH_BASE']='whoosh'
app.config['SECRET_KEY'] = 'KJNF0128YURT08TN8G20TY0H0'          # can be ignored for now serves no purpose yet

db = SQLAlchemy(app)						# final initialization step of the database db, db is now the database
#bcrypt = Bcrypt(app)
cnx = mysql.connector.connect(user='dbtest4020', password='Pp0gHfo-~149', host='den1.mysql1.gear.host', database='dbtest4020', use_pure=True)
genres = ['Rock', 'Metal', 'Country', 'Electronic', 'Blues', 'Dance', 'Hip-Hop/Rap']

loggedin=0						# int flags to see if someone is logged in or not 1 logged in 0 not logged in
ismod=0							# int flag to mark if they are moderator or not 1 is 0 isnt
startuser = "Not Logged In"

posts = [						# most recent needs to be top post, announcement posts
	 {
                'author': 'Chris Osterer',
                'title': 'Event Photos!',
                'content': 'Photos from our recent events can be found below!',
                'date_posted': '30 November 2018'
        },
	 {
                'author': 'Chris Osterer',
                'title': 'New Search features!',
                'content': 'We have added additional search features under the Artist and Concerts Pages!',
                'date_posted': '18 November 2018'
        },
	{
		'author': 'Chris Osterer',
		'title': 'Database Additions',
		'content': 'We are please to anounce that we have added hundreds of your favorite artists to our site!',
		'date_posted': '16 November 2018'
	},
	{
                'author': 'Chris Osterer',
                'title': 'FestivalFinder Grand Opening!',
                'content': 'We are pleased to announce the Launching of FestivalFinder!',
		'date_posted': '23 October 2018'
        }
]

class Results(Table):				# these classes are used to form tables to be displayed on webpage based on sql queries by web page users
	artistsname = Col('artistsanme')
	genre = Col('genre')
	nummembers = Col('nummembers')

class UserResults(Table):
	username = Col('username')
	email = Col('email')
	standing = Col('standing')

class bandResults(Table):
	name = Col('name')
	websiteURL = Col('websiteURL')
	spotifyURL = Col('spotifyURL')
	founded = Col('founded')
	genre=Col('genre')
	active = Col('active')

class SongResults(Table):
	songName = Col('songName')
	bandName = Col('bandname')
	album = Col('album')
	runtime = Col('runtime')

class festivalResults(Table):
	name = Col('name')
	startDate = Col('startDate')
	location = Col('location')
	websiteURL = Col('websiteURL')

class festivalSchResults(Table):
	festivalName = Col('festivalname')
	festivalStart = Col('festivalStart')
	bandName = Col('bandName')
	performanceTime = Col('performanceTime')

class favoritedSongs(Table):
	user = Col('user')
	song = Col('song')
	band = Col('band')
	album = Col('album')

class BandModList(Table):
	moderator = Col('moderator')
	bandName = Col('bandName')

class festModList(Table):
	moderator = Col('moderator')
	festivalName = Col('festivalName')

class AdminList(Table):
	username = Col('username')

@app.route("/")
@app.route("/Home")										# 127.0.0.1/Home
def home():
        return render_template('home.html', posts = posts, isLogged=loggedin, startuser = startuser, isMod=ismod)

@app.route("/About")
def about():
        return render_template('about.html', title = 'About', isLogged=loggedin, startuser= startuser, isMod = ismod)

@app.route("/Contact")
def contact():
        return render_template('contact.html', title = 'Contact Us', isLogged=loggedin, startuser = startuser, isMod=ismod)

@app.route("/Festivals", methods=['GET', 'POST'])
def festivals():										# search these by: zip ....
	if request.method == 'POST':
		formtext = request.form['zipquery']
		#sqls = text('select * from testtable where persname="'+ formtext  +'";')       # text(<sequel query here>)
		sqls = text('select * from artists;')                                       	# text(<sequel query here>)
		rows = db.engine.execute(sqls)                                                  # gets the rows that match the search
		table = Results(rows)
		#table = bandResults(rows)
		table.border= True
		return render_template('festivals.html', table=table, posts=posts, genres=genres, isLogged=loggedin, isMod=ismod)          # displays rows and the colors list localhost/search
	else:
		return render_template('festivals.html', posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)


@app.route("/Bands", methods= ['GET','POST'])										      # should show two different pages one for regtular user na done for mods
def bands():
	global startuser
	global loggedin
	global ismod
	form = ModRegistrationForm()
	if(ismod):
		if form.validate_on_submit():
			if(createAccount(cnx, form.username.data, form.password.data, form.email.data)):
				flash('Your account has been created! You may now log in!', 'success')
			else:
				flash('Error Creating Account, Please Retry with Different Username', 'success')
				#return redirect(url_for('home'))
			return render_template('modbands.html', posts=posts, form = form, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)													      # actions for a  mod
		else:
			if request.method == 'POST':                                                                                  # if they fill out a text field
				formtext = request.form['query']
				sqls = text('select * from Band where name="'+ formtext  +'";')                                       # text(<sequel query here>)
				rows = db.engine.execute(sqls)                                                                        # gets the rows that match the search
				table = bandResults(rows)
				table.border= True
				return render_template('modbands.html', table=table, form=form, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)              # displays rows and $
			return render_template('modbands.html', form=form, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
	else:
		if request.method == 'POST':										      # if they fill out a text field
			formtext = request.form['query']
			sqls = text('select * from Band where name="'+ formtext  +'";')                                       # text(<sequel query here>)
			rows = db.engine.execute(sqls)                                                  		      # gets the rows that match the search
			table = bandResults(rows)
			table.border= True
			return render_template('bands.html', table=table, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)          	# displays rows and the colors list localhost/search
		else:
			return render_template('bands.html', posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		if(createAccount(cnx, form.username.data, form.password.data, form.email.data)):
			flash('Your account has been created! You may now log in!', 'success')
		else:
			flash('Error Creating Account, Please Retry with Different Username', 'success')
		return redirect(url_for('home'))											# redirect to home pg on succesful log in
	return render_template('register.html', title='Register', form=form, isLogged=loggedin, startuser = startuser, isMod=ismod )

@app.route("/login", methods=['GET', 'POST'])
def login():
	global loggedin
	global startuser
	global ismod
	form = LoginForm()
	if form.validate_on_submit():
		if (checkPassword(cnx, form.username.data, form.password.data)):
			flash('YOU have been logged in', 'success')
			loggedin = 1
			if(form.username.data == "ccc"):								# should check for moderator here
				ismod=1
			startuser = form.username.data                                                                  # set the startuser to the name they type in for suername
			return redirect(url_for('home'))								# redirect to home pg on succesful log in
		else:
			flash('Login Unsuccessful, Check username and password', 'danger')				# log in error
	return render_template('login.html', title='Login', form=form, isLogged=loggedin, startuser = startuser, isMod=ismod)

@app.route("/logout")
def logout():
	global ismod
	global loggedin
	global startuser
	startuser = "Not Logged In"
	loggedin = 0
	ismod=0
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)

