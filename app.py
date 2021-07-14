"""Blogly application."""

from flask import Flask, render_template, redirect, request
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
def redirect_homepage():
    """Redirects to page that loads our homepage"""
    return redirect( "/users")

@app.route('/users')
def load_homepage():
    """Loads our homepage"""


    #emp user.query.all() DOUBLE CHECK TODO
    users = User.query.all()
    return render_template(
        "users.html", 
        users = users
    )

@app.route('/users/new', methods = ['GET','POST'])
def load_create_user_form():
    """Loads create user page and our create user form"""
    if Flask.request.method == 'GET':
        return render_template("add_users.html")

    elif Flask.request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        if image_url == "":
            image_url = None 

        new_user =  User(first_name,last_name,image_url)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect("/users")
    
@app.route('users/<user_id>')
def show_user_info(user_id):
    user = User.query.get(user_id)

    return render_template(
        "user_details.html",
        user = user
    )

@app.route('')
    
    

