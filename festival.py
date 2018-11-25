from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_table import Table, Col
import flask_whooshalchemy as wa


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01Sda&hw@localhost/testdb'

#tring to copnnect to gearhost database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://costerertestdb:Ik6N-wXcGo7_@den1.mysql6.gear.host/costerertestdb'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE']='whoosh'
db = SQLAlchemy(app)						# final initialization step of the database db, db is now the database


app.config['SECRET_KEY'] = 'KJNF0128YURT08TN8G20TY0H0'		# can be ignored for now serves no purpose yet

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


class Results(Table):
	persname = Col('persname')


class testtable(db.Model):					# we will have classes for each table, testtable is a single table with a persname column
	__tablename__ = 'testtable'
	__searchable__ = ['persname']				# n ames of columns that will be searchable
	persname = db.Column(db.String(255), primary_key=True)

wa.whoosh_index(app, testtable) 					#Post is the name of the above class, this can be removed serves no purpose



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


@app.route("/Concerts", methods=['GET'])
def concerts():								# search these by: zip ....
        return render_template('concerts.html', posts = posts, colors=colors )

@app.route("/Artists")
def artists():
        return render_template('artists.html', title = 'About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(("Account Created for {form_username_data}").format(form_username_data=form.username.data), 'success')
		return redirect(url_for('home'))					# redirect to home pg on succesful log in
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('YOU have been logged in', 'success')
			return redirect(url_for('home'))				# redirect to home pg on succesful log in
		else:
			flash('Login Unsuccessful, Check username and password', 'danger')	# log in error
	return render_template('login.html', title='Login', form=form)

@app.route('/search' , methods=['GET', 'POST'])
def search():
	if request.method == 'POST':
		#rows = testtable.query.whoosh_search(request.args.get('query')).all()		# this may not do what you think it does
		#rows = testtable.query.all()
		formtext = request.form['query']
		sqls = text('select * from testtable where persname="'+ formtext  +'";')					# text(<sequel query here>)
		rows = db.engine.execute(sqls)							# gets the rows that match the search
		table = Results(rows)
		table.border= True
		return render_template('search.html', table=table, posts=posts, colors=colors)		# displays rows and the colors list localhost/search
	else:
		return render_template('search.html', posts=posts, colors=colors) 

if __name__ == '__main__':								# main function
	app.run(debug=True)

