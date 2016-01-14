from __future__ import print_function
from flask import Flask, flash, g, render_template, request, url_for
import psycopg2

# Application SetUP\p
app = Flask(__name__)
app.config.from_pyfile('config.py')

# DATABASE
def connect_db():
    return psycopg2.connect(database="improv_reg", user="nick", password="zeP7aicoopa", host="127.0.0.1")

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
        first_name, last_name, email_address = request.form.values()
        sql_statement = "INSERT INTO guests (guest_id, first_name, last_name, email_address) VALUES (DEFAULT, %s, %s, %s)"
        cur = g.db.cursor()
        cur.execute(sql_statement, (first_name, last_name, email_address))
        g.db.commit()
        flash('You have successfully registered.')
    return render_template('registration_form.html', error=error)


@app.route('/guests')
def show_guests():
    cur = g.db.cursor()
    cur.execute("SELECT * FROM guests;")
    guests = [dict(first_name=row[1], last_name=row[2], email_address=row[3]) for row in cur.fetchall()]
    cur.close()
    return render_template('show_guests.html', guests=guests)


# Fire up server if file ran as standalone application.
if __name__ == '__main__':
    app.run()
