from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import flask_whooshalchemy as wa


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01Sda&hw@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['WHOOSH_BASE']='whoosh'
db = SQLAlchemy(app)


app.config['SECRET_KEY'] = 'KJNF0128YURT08TN8G20TY0H0'

posts = [

	{
		'author': 'chris osterer',
		'title': 'heelo py',
		'content': 'the content',
		'date_posted': '23 October 1992'
	},

	{
                'author': 'chris bossterer',
                'title': 'heelllllo pyo',
                'content': 'the contentx',
		'date_posted': '23 October 1992'
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
