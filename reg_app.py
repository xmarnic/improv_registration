from __future__ import print_function
from flask import Flask, flash, g, render_template, request, url_for
from contextlib import closing
import sqlite3


# Application SetUP\p
app = Flask(__name__)
app.config.from_pyfile('config.py')


# DATABASE
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Create database with Python as opposed to sqlite3
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Connect to db before each request
@app.before_request
def before_request():
    g.db = connect_db()

# Close db after request
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# VIEWS
@app.route('/', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        g.db.execute('insert into guests (first_name, last_name, email_address) values (?, ?, ?)',
                     [request.form['first_name'], request.form['last_name'], request.form['email']])
        g.db.commit()
        flash('You have successfully registered.')
    return render_template('registration_form.html', error=error)


@app.route('/guests')
def show_guests():
    cur = g.db.execute('select first_name, last_name, email_address from guests order by id desc')
    guests = [dict(first_name=row[0], last_name=row[1], email_address=row[2]) for row in cur.fetchall()]
    return render_template('show_guests.html', guests=guests)


# Fire up server if file ran as standalone application.
if __name__ == '__main__':
    app.run()
