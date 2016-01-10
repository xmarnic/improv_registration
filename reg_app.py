from __future__ import print_function
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return render_template('index.html')


# Fire up server if file ran as standalone application.
if __name__ == '__main__':
    app.run()
