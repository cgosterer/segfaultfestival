import mysql.connector
import random
import time

from hashlib import sha256 as userHash
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, ModRegistrationForm, SongForm, UserSongForm, UnlikeSongForm, UserBandForm, UnlikeBandForm, DispBandsForm, DispSongsForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_table import Table, Col

from mysql.connector.cursor import MySQLCursorPrepared

from accountAccess import checkExists, checkModExists, checkPassword, createAccount
from userFunctions import getLikeCount, like, likeSong, unlinkeBand, unlikeSong, createPage
from bandModify import addSong, removeSong, updateFoundingDate, setActive, setInactive, addMod, removeMod, setSpotify, setWebsite

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbtest4020:Pp0gHfo-~149@den1.mysql1.gear.host/dbtest4020'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY'] = 'KJNF0128YURT08TN8G20TY0H0'          # can be ignored for now serves no purpose yet

db = SQLAlchemy(app)						# final initialization step of the database db, db is now the database
cnx = mysql.connector.connect(user='dbtest4020', password='Pp0gHfo-~149', host='den1.mysql1.gear.host', database='dbtest4020', use_pure=True)

genres = ['Rock', 'Metal', 'Country', 'Electronic', 'Blues', 'Dance', 'Hip-Hop/Rap']

loggedin=0						# int flags to see if someone is logged in or not 1 logged in 0 not logged in
ismod=0							# int flag to mark if they are moderator or not 1 is 0 isnt
startuser = "cnn"

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
                'content': 'We have added additional search features under the Bands, Concerts, and Festivals Pages!',
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
	#runtime = Col('runtime')		# This Will crash the program if attempted to be acquired from an sql query so we cannot display runtimes will fix  if more important things are done

class festivalResults(Table):
	name = Col('name')
	#startDate = Col('startDate')
	location = Col('location')
	websiteURL = Col('websiteURL')
	zipCode = Col('zipCode')

class festivalSchResults(Table):
	festivalName = Col('festivalname')
	festivalStart = Col('festivalStart')
	bandName = Col('bandName')
	performanceTime = Col('performanceTime')

class favsongsresults(Table):
	user = Col('user')
	song = Col('song')
	band = Col('band')
	album = Col('album')

class favbandsresults(Table):
	bandName = Col('bandeName')
	username = Col('username')

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
		nametext = request.form.get('namequery')
		ziptext = request.form.get('zipquery')
		citytext = request.form.get('cityquery')

		# the following block is desinged to return empty tables
		nameq = text('select songName, bandName, album from Song where songName="songnameinourdbtest4020databse";')     # this will never happen can use to get empty result
		namerows = db.engine.execute(nameq)
		nametable = SongResults(namerows)
		nametable.border= True
		zipq = text('select songName, bandName, album from Song where bandName="songnameinourdbtest4020databse";')
		ziprows = db.engine.execute(zipq)
		ziptable = SongResults(ziprows)
		ziptable.border= True
		cityq =text('select songName, bandName, album from Song where album="songnameinourdbtest4020databse";')        # if someone names an album this i will eat a shoe
		cityrows = db.engine.execute(cityq)
		citytable = SongResults(cityrows)
		citytable.border= True
		# empty tables have been formed as of this line

		if(nametext):
			nameq = text('select name, location, websiteURL, zipCode from Festival where name="'+ nametext  +'";')
			namerows = db.engine.execute(nameq)
			nametable = festivalResults(namerows)
			nametable.border= True
		if(ziptext):
			zipq = text('select name, location, websiteURL, zipCode from Festival where zipcode="'+ ziptext  +'";') # this may be wrong as zip is stored as an int
			ziprows = db.engine.execute(zipq)
			ziptable = festivalResults(ziprows)
			ziptable.border= True
		if(citytext):
			cityq =text('select name, location, websiteURL, zipCode from Festival where location="'+ citytext  +'";')
			cityrows = db.engine.execute(cityq)
			citytable = festivalResults(cityrows)
			citytable.border= True
		return render_template('festivals.html', ziptable=ziptable, citytable=citytable, nametable=nametable, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
	else:
		return render_template('festivals.html', posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)


@app.route("/Bands", methods= ['GET','POST'])										      # should show two different pages one for regtular user na done for mods
def bands():
	global startuser
	global loggedin
	global ismod
	form = ModRegistrationForm()
	userbandform = UserBandForm()
	unlikebandform = UnlikeBandForm()										# the forms displayed on the mod pages
	if(ismod):
		if form.validate_on_submit():
			if(createAccount(cnx, form.username.data, form.password.data, form.email.data)):
				if( addMod(cnx, form.bandname.data, form.username.data) ):
					flash('Your Moderator Account  has been created!', 'success')
			else:
				flash('Error Creating Account, Please Retry with Different Username', 'success')
				return redirect(url_for('home'))
			return render_template('modbands.html', posts=posts, form=form, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)													      # actions for a  mod
		if request.method == 'POST':                                                                                  # if they fill out a text field
			formtext = request.form['query']
			sqls = text('select * from Band where name="'+ formtext  +'";')                                       # text(<sequel query here>)
			rows = db.engine.execute(sqls)                                                                        # gets the rows that match the search
			table = bandResults(rows)
			table.border= True
			return render_template('modbands.html', table=table, form=form, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)              # displays rows and $
		return render_template('modbands.html', form=form, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
	else:
		if userbandform.validate_on_submit():
			if (loggedin == 0):                                                             # can only add favorites when logged in
				flash('Please Log in to add Band to favorites!', 'danger')
				return render_template('bands.html', posts=posts, userbandform=userbandform, unlikebandform=unlikebandform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
			if( like(cnx, userbandform.bandname.data, startuser)):
				flash('Band added to favorites List!', 'success')
			else:                                                                   # create fav song fails
				flash('Error Adding Favorite Band Please retry', 'danger')
			return render_template('bands.html', posts=posts, userbandform=userbandform, unlikebandform=unlikebandform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
		if unlikebandform.validate_on_submit():
			if(loggedin == 0):
				flash('Please Log in to remove a Band from favorites!', 'danger')
				return render_template('bands.html', posts=posts, userbandform=userbandform, unlikebandform=unlikebandform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
			if(unlinkeBand(cnx, startuser, unlikebandform.ubandname.data)):
				flash('Band Succesfully Removed', 'success')
			else:
				flash('Error Removing Band from Favorites Please retry', 'danger')      # error trying to unlike Band
			return render_template('bands.html', posts=posts, userbandform=userbandform, unlikebandform=unlikebandform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
		if request.method == 'POST':										      # if they fill out a text field
			formtext = request.form['query']
			sqls = text('select * from Band where name="'+ formtext  +'";')                                       # text(<sequel query here>)
			rows = db.engine.execute(sqls)                                                  		      # gets the rows that match the search
			table = bandResults(rows)
			table.border= True
			return render_template('bands.html', userbandform=userbandform, unlikebandform=unlikebandform, table=table, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)          	# displays rows and the colors list localhost/search
		else:
			return render_template('bands.html', userbandform=userbandform, unlikebandform=unlikebandform, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)

@app.route("/Songs", methods= ['GET','POST'])
def songs():
	global startuser
	global loggedin
	global ismod
	songform = SongForm()										# creates a song for a band from a moderator
	usersongform= UserSongForm()
	unlikesongform = UnlikeSongForm()
	dispsongsform = DispSongsForm()
	if(ismod):
		if songform.validate_on_submit():
			if(addSong( cnx, songform.bandname.data, songform.songname.data, songform.album.data)):  #if error with runtime just change to generic value
				flash('Your Song has been created!', 'success')					 # tab over when fixed
			else:											 # if create favorite song fails
				flash('Error Creating Song Please retry', 'danger')
			return render_template('modsongs.html', posts=posts, songform=songform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
		else:
			if request.method == 'POST':
				nametext = request.form.get('namequery')
				bandtext = request.form.get('bandquery')
				albumtext = request.form.get('albumquery')
				nameq = text('select songName, bandName, album from Song where songName="songnameinourdbtest4020databse";')     # this will never happen can use to get empty result
				namerows = db.engine.execute(nameq)
				nametable = SongResults(namerows)
				nametable.border= True
				bandq = text('select songName, bandName, album from Song where bandName="songnameinourdbtest4020databse";')
				bandrows = db.engine.execute(bandq)
				bandtable = SongResults(bandrows)
				bandtable.border= True
				albumq =text('select songName, bandName, album from Song where album="songnameinourdbtest4020databse";')        # if someone names an album this i will eat a shoe
				albumrows = db.engine.execute(albumq)
				albumtable = SongResults(albumrows)
				albumtable.border= True

				if(nametext):
					nameq = text('select songName, bandName, album from Song where songName="'+ nametext  +'";')
					namerows = db.engine.execute(nameq)
					nametable = SongResults(namerows)
					nametable.border= True
				if(bandtext):
					bandq = text('select songName, bandName, album from Song where bandName="'+ bandtext  +'";')
					bandrows = db.engine.execute(bandq)
					bandtable = SongResults(bandrows)
					bandtable.border= True
				if(albumtext):
					albumq =text('select songName, bandName, album from Song where album="'+ albumtext  +'";')
					albumrows = db.engine.execute(albumq)
					albumtable = SongResults(albumrows)
					albumtable.border= True
				return render_template('modsongs.html', nametable=nametable, bandtable=bandtable, albumtable=albumtable, songform=songform, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
			else:
				return render_template('modsongs.html', songform=songform, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
	else:
		if dispsongsform.validate_on_submit():
			if(loggedin == 0):
				flash('Please Log in to View favorites!', 'danger')
				return render_template('songs.html', posts=posts, usersongform=usersongform, unlikesongform=unlikesongform, dispsongsform=dispsongsform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
			favq = text('select user, song, band, album from FavoritedSongs where user="' + startuser + '";')
			favrows = db.engine.execute(favq)
			favtable = favsongsresults(favrows)
			favtable.border = True
			return render_template('favsongs.html', favtable=favtable, posts=posts, dispsongsform=dispsongsform, usersongform=usersongform, unlikesongform=unlikesongform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
		if usersongform.validate_on_submit():
			if (loggedin == 0):								# can only display favorites when logged in
				flash('Please Log in to add Song to favorites!', 'danger')
				return render_template('songs.html', posts=posts, usersongform=usersongform, dispsongsform=dispsongsform, unlikesongform=unlikesongform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
			if( likeSong(cnx, startuser, usersongform.songname.data, usersongform.bandname.data, usersongform.album.data)):
				flash('Song added to favorites List!', 'success')
			else:									# create fav song fails
				flash('Error Adding Favorite Song Please retry', 'danger')
			return render_template('songs.html', posts=posts, usersongform=usersongform, unlikesongform=unlikesongform, dispsongsform=dispsongsform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
		if unlikesongform.validate_on_submit():
			if(loggedin == 0):
				flash('Please Log in to Remove a Song from favorites!', 'danger')
				return render_template('songs.html', posts=posts, usersongform=usersongform, unlikesongform=unlikesongform, dispsongsform=dispsongsform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
			if(unlikeSong(cnx, startuser, unlikesongform.usongname.data, unlikesongform.ubandname.data, unlikesongform.ualbumname.data)):
				flash('Song Succesfully Removed', 'success')
			else:
				flash('Error Removing Song from Favorites Please retry', 'danger')	# error trying to unlike a song
			return render_template('songs.html', posts=posts, usersongform=usersongform, unlikesongform=unlikesongform, dispsongsform=dispsongsform, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod)
		if request.method == 'POST':								# if they used one of the text searches
			nametext = request.form.get('namequery')
			bandtext = request.form.get('bandquery')
			albumtext = request.form.get('albumquery')

			nameq = text('select songName, bandName, album from Song where songName="songnameinourdbtest4020databse";')	# this will never happen can use to get empty result
			namerows = db.engine.execute(nameq)
			nametable = SongResults(namerows)
			nametable.border= True
			bandq = text('select songName, bandName, album from Song where bandName="songnameinourdbtest4020databse";')
			bandrows = db.engine.execute(bandq)
			bandtable = SongResults(bandrows)
			bandtable.border= True
			albumq =text('select songName, bandName, album from Song where album="songnameinourdbtest4020databse";')	# if someone names an album this i will eat a shoe
			albumrows = db.engine.execute(albumq)
			albumtable = SongResults(albumrows)
			albumtable.border= True

			if(nametext):
				nameq = text('select songName, bandName, album from Song where songName="'+ nametext  +'";')
				namerows = db.engine.execute(nameq)
				nametable = SongResults(namerows)
				nametable.border= True
			if(bandtext):
				bandq = text('select songName, bandName, album from Song where bandName="'+ bandtext  +'";')
				bandrows = db.engine.execute(bandq)
				bandtable = SongResults(bandrows)
				bandtable.border= True
			if(albumtext):
				albumq =text('select songName, bandName, album from Song where album="'+ albumtext  +'";')
				albumrows = db.engine.execute(albumq)
				albumtable = SongResults(albumrows)
				albumtable.border= True
			return render_template('songs.html', dispsongsform=dispsongsform, unlikesongform=unlikesongform, usersongform=usersongform, nametable=nametable, bandtable=bandtable, albumtable=albumtable, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod) # displays page with table
		else:
			return render_template('songs.html', unlikesongform=unlikesongform, dispsongsform=dispsongsform, usersongform=usersongform, posts=posts, genres=genres, isLogged=loggedin, startuser=startuser, isMod=ismod) #displays page without the table as no table has been created yet

@app.route("/register", methods=['GET', 'POST'])
def register():																# must use '1' when creating standing
	form = RegistrationForm()
	if form.validate_on_submit():
		if(createAccount(cnx, form.username.data, form.password.data, form.email.data)):
			flash('Your account has been created! You may now log in!', 'success')
		else:
			flash('Error Creating Account, Please Retry with Different Username', 'danger')
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
			#if(form.username.data == "ccc"):								# should check for moderator here with function that we create
			if(checkModExists(cnx, form.username.data)):
				ismod=1											# can still set this too one if they are a mod
			startuser = form.username.data                                                                  # set the startuser to the name they type in for suername
			return redirect(url_for('home'))								# redirect to home pg on succesful log in
		else:
			flash('Login Unsuccessful, Check username and password', 'danger')				# log in error
	return render_template('login.html', title='Login', form=form, isLogged=loggedin, startuser = startuser, isMod=ismod)			# taked us back to login page

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

