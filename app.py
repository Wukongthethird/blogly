"""Blogly application."""

from flask import Flask, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()


@app.route('/')
def load_homepage():
    """Loads our homepage"""

    """TODO: need to change to redirect"""
    return render_template(
        "users.html"
    )




@app.route('/users/new')
def load_create_user_form():
    """Loads create user page and our create user form"""

    return render_template(
        
    )