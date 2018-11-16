from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01Sda&hw@localhost/testdb'

#tring to copnnect to gearhost database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://costerertestdb:Ik6N-wXcGo7_@den1.mysql6.gear.host/costerertestdb'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE']='whoosh'
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = 'KJNF0128YURT08TN8G20TY0H0'

posts = [						# most recent needs to be top post


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


class testtable(db.Model):
	__tablename__ = 'testtable'
	__searchable__ = ['persname']				# names of columns that will be searchable
	persname = db.Column(db.String(255), primary_key=True)

wa.whoosh_index(app, testtable) 					#Post is the name of the above class



@app.route("/")
@app.route("/Home")
def home():
        return render_template('home.html', posts = posts)

@app.route("/About")
def about():
        return render_template('about.html', title = 'About')

@app.route("/Contact")
def contact():
        return render_template('contact.html', title = 'Contact Us')


@app.route("/Concerts")
def concerts():
        return render_template('concerts.html', posts = posts)

@app.route("/Artists")
def artists():
        return render_template('artists.html', title = 'About')


@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(("Account Created for {form_username_data}").format(form_username_data=form.username.data), 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'admin@blog.com' and form.password.data == 'password':
			flash('YOU have been logged in', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful, Check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/search')
def search():
	#rows = testtable.query.whoosh_search(request.args.get('query'))		# this may not do what you think it does
	rows = testtable.query.all()
	return render_template('search.html', rows = rows)

if __name__ == '__main__':
	app.run(debug=True)
