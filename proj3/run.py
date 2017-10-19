
from flask import Flask, render_template, flash, redirect, Response, request, url_for, Markup
from flask_wtf import FlaskForm
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
from wtforms.fields import SubmitField
from flask_login import LoginManager, login_required
from datetime import datetime
import sqlite3
from functools import wraps
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
pagedown = PageDown(app)
login_manager = LoginManager()
login_manager.init_app(app)


def check_auth(username, password):
    return username == 'pinto' and password == 'beans'
    #this is where could add search into a user table with passwords 

def authenticate():
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

class PageDownForm(FlaskForm):
    pagedown = PageDownField('Title')
    pagedown2 = PageDownField('Post')
    submit = SubmitField('Submit')

@app.route('/', methods=['POST', 'GET'])
@app.route('/index/', methods=['GET', 'POST'])
@requires_auth
def index():
    form = PageDownForm()
    text1 = None
    text2 = None
    text3 = None
    username = 'pinto'
    rows = None
    if form.validate_on_submit():
      text1 = form.pagedown.data
      text2 = form.pagedown2.data
      text3 = datetime.now().strftime('%B %d, %Y at %I:%M %p')
      c = sqlite3.connect('pete.db')
      c.execute("INSERT INTO posts(user, title, post, date_posted) VALUES(?,?,?,?);", (username, text1, text2, text3))
      c.commit()
      c.close()
    
    c = sqlite3.connect('pete.db')
    cur = c.execute('SELECT * FROM posts ORDER BY date_posted DESC')
    rows = cur.fetchall()

    return render_template('index.html', username=username, form=form, text1=text1, text2=text2, text3=text3, rows=rows)

@app.route('/logout/', methods=['GET'])
def authenticate():
    return Response(
    'That was totally rad! See you next time.', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(debug=True)