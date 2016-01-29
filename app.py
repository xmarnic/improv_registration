from __future__ import print_function
from flask import Flask, flash, g, redirect, render_template, request, url_for
from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import Required, Email
import os
import psycopg2
import urlparse


# Application SetUP\p
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Forms
class RegForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    email = StringField('Email Address', validators=[Required(), Email()])
    city = StringField('City', validators=[Required()])
    public = BooleanField('Public')


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
@app.route('/')
def root_redirect():
    """Quick hack, will register a blueprint before production deploy :("""
    return redirect(url_for('register'))

@app.route('/theatre', methods=['GET', 'POST'])
def register():
    alert_class = None
    form = RegForm()
    if form.validate_on_submit():
        sql_statement = "INSERT INTO guests (first_name, last_name, email_address, city, public) VALUES (%s, %s, %s, %s, %s)"
        cur = g.db.cursor()
        cur.execute(sql_statement, (form.first_name.data.capitalize(),
            form.last_name.data.capitalize(), form.email.data.lower(),
            form.city.data.capitalize(), form.public.data)
        )
        g.db.commit()
        cur.close()
        alert_class = 'alert-success'
        flash('You have successfully registered.')
        return redirect(url_for('show_guests'))
    elif request.method == 'POST':
        alert_class='alert-danger'
        flash('Please complete the registration form.')
    return render_template('reg_form.html', form=form, alert_class=alert_class, hidden=None)

@app.route('/theatre/guestlist')
def show_guests():
    cur = g.db.cursor()
    cur.execute("SELECT first_name, last_name, city FROM guests WHERE public")
    guests = [dict(first_name=row[0], last_name=row[1], city=row[2]) for row in cur.fetchall()]
    cur.close()
    return render_template('guestlist.html', guests=guests, alert_class='alert-success', hidden='hidden')


# Fire up server if file ran as standalone application.
if __name__ == '__main__':
    app.run()
