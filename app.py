from __future__ import print_function
from flask import Flask, flash, g, render_template, request, url_for
import os
import psycopg2
import urlparse


# Application SetUP\p
app = Flask(__name__)
app.config.from_pyfile('config.py')

# DATABASE
def connect_db():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
    )
    return conn


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
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email_address = request.form['email']
        sql_statement = "INSERT INTO guests (first_name, last_name, email_address) VALUES (%s, %s, %s)"
        cur = g.db.cursor()
        cur.execute(sql_statement, (first_name, last_name, email_address))
        g.db.commit()
        flash('You have successfully registered.')
    return render_template('registration_form.html', error=error)


@app.route('/guests')
def show_guests():
    cur = g.db.cursor()
    cur.execute("SELECT * FROM guests")
    guests = [dict(first_name=row[0], last_name=row[1], email_address=row[2]) for row in cur.fetchall()]
    cur.close()
    return render_template('show_guests.html', guests=guests)


# Fire up server if file ran as standalone application.
if __name__ == '__main__':
    app.run()
