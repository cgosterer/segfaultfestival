from flask import Flask, render_template
app = Flask(__name__)

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



@app.route("/")
@app.route("/Home")
def home():
        return render_template('home.html', posts = posts)

@app.route("/About")
def about():
        return render_template('about.html', title = 'About')

if __name__ == '__main__':
	app.run(debug=True)
