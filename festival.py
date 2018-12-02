import mysql.connector
import random
import time
from hashlib import sha256 as userHash
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_table import Table, Col
from flask_bcrypt import Bcrypt
from mysql.connector.cursor import MySQLCursorPrepared

from accountAccess import checkExists, checkPassword, createAccount

#import flask_whooshalchemy as wa

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://costerertestdb:Ik6N-wXcGo7_@den1.mysql6.gear.host/costerertestdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE']='whoosh'
app.config['SECRET_KEY'] = 'KJNF0128YURT08TN8G20TY0H0'          # can be ignored for now serves no purpose yet

db = SQLAlchemy(app)						# final initialization step of the database db, db is now the database
bcrypt = Bcrypt(app)

cnx = mysql.connector.connect(user='costerertestdb', password='Ik6N-wXcGo7_', host='den1.mysql6.gear.host', database='costerertestdb', use_pure=True)



colors = ['red', 'blue', 'green', 'yellow']


posts = [						# most recent needs to be top post, announcement posts


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

#class User(db.Model):								# this probably wont be needed
	#username = db.column(db.string(50), unique=True, nullable = False)
	#email = db.column(db.string(255), unique=False, nullable = False)
	#hash = db.column(db.string(64), unique=False, nullable = False)
	#salt = db.column(db.Integer,unique= False, nullable=False)
	#standing= db.column(db.Boolean,unqiue = False, nullable = False)

	#def __repr__(self):
		#return f"User('{self.username}', '{self.email}')"


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
@app.route("/Home")						# 127.0.0.1/Home
def home():
        return render_template('home.html', posts = posts)

@app.route("/About")
def about():
        return render_template('about.html', title = 'About')

@app.route("/Contact")
def contact():
        return render_template('contact.html', title = 'Contact Us')


@app.route("/Festivals", methods=['GET', 'POST'])
def festivals():								# search these by: zip ....
	if request.method == 'POST':
		#rows = testtable.query.whoosh_search(request.args.get('query')).all()          # this may not do what you think it does
		#rows = testtable.query.all()
		formtext = request.form['query']
		#sqls = text('select * from testtable where persname="'+ formtext  +'";')                                       # text(<sequel query here>)
		sqls = text('select * from artists;')                                       # text(<sequel query here>)
		rows = db.engine.execute(sqls)                                                  # gets the rows that match the search
		table = Results(rows)
		#table = bandResults(rows)
		table.border= True
		return render_template('festivals.html', table=table, posts=posts, colors=colors)          # displays rows and the colors list localhost/search
	else:
		return render_template('festivals.html', posts=posts, colors=colors) 


@app.route("/Bands", methods= ['GET','POST'])
def bands():
	if request.method == 'POST':
		#rows = testtable.query.whoosh_search(request.args.get('query')).all()          # this may not do what you think it does
		#rows = testtable.query.all()
		formtext = request.form['query']
		#sqls = text('select * from testtable where persname="'+ formtext  +'";')                                       # text(<sequel query here>)
		sqls = text('select * from artists;')                                       # text(<sequel query here>)
		rows = db.engine.execute(sqls)                                                  # gets the rows that match the search
		table = Results(rows)
		#table = bandResults(rows)
		table.border= True
		return render_template('bands.html', table=table, posts=posts, colors=colors)          # displays rows and the colors list localhost/search
	else:
		return render_template('bands.html', posts=posts, colors=colors) 

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		if(createAccount(cnx, form.username.data, form.password.data, form.email.data)):
			flash('Your account has been created! You may now log in!', 'success')
		else:
			flash('Error Creating Account, Please Retry with Different Username', 'success')

		return redirect(url_for('home'))					# redirect to home pg on succesful log in
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if (checkPassword(cnx, form.username.data, form.password.data)):
			flash('YOU have been logged in', 'success')
			return redirect(url_for('home'))				# redirect to home pg on succesful log in
		else:
			flash('Login Unsuccessful, Check username and password', 'danger')	# log in error
	return render_template('login.html', title='Login', form=form)



if __name__ == '__main__':								# main function
	app.run(debug=True)

