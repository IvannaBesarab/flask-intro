from flask import Flask, flash, session, g, render_template, redirect, url_for, request
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps

import sqlite3

app = Flask(__name__)

app.secret_key = 'my security key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'slqlite3:///posts.db'
#create the sqlalchemy object
db  = SQLAlchemy(app)
#app.database = "sample.db"

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap


def connect_db():
	return sqlite3.connect('sample.db')

@app.route('/')
@login_required
def home():
	#return "Hello World"
	post_dict ={}
	posts = []
	try:
		g.db = connect_db()
		cur = g.db.execute('select * from posts')
		#print cur
		#print cur.fetchall()
		
		for row in cur.fetchall():
			#post_dict['title'] = row[0]
			#post_dict['description'] = row[1]
			posts.append(dict(title=row[0], description=row[1]))
			#print posts
		#posts = [dict(title = row[0], description = row[1]) for row in cur.fetchall()]
		#print posts
		g.db.close()
	except sqlite3.OperationalError:
		flash('You have no database!')
	return render_template("index.html", posts = posts)


@app.route('/welcome')
def welcome():
	return render_template("welcome.html")



@app.route('/login', methods = ['GET','POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin': 
			error = 'Invalod credentails. Please try again'
		else:
			session['logged_in'] = True
			flash('You were logged in!')
			return redirect(url_for('home'))
	return render_template('login.html', error = error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash('You were just logged out!')
	return redirect(url_for('welcome'))


if __name__ == '__main__':
	app.run(debug=True)