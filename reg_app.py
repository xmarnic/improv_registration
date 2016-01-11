from __future__ import print_function
from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass
    else:
        return render_template('register.html')


# Fire up server if file ran as standalone application.
if __name__ == '__main__':
    app.run()
