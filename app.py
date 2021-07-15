"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension


#  from test_model import db, connect_db, User
#  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
#  this will connect to test_db
#  reference the standard model and db is how to revert


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def redirect_homepage():
    """Redirects to page that loads our homepage"""

    return redirect( "/users")

@app.route('/users')
def load_homepage():
    """Loads our homepage"""

    #emp user.query.all() DOUBLE CHECK TODO
    users = User.query.order_by( User.last_name).all()
    return render_template(
        "users.html", 
        users=users
    )

@app.route('/users/new', methods = ['GET','POST'])
def load_create_user_form():
    """Loads create user page and our create user form"""

    if request.method == 'GET':
        return render_template("add_users.html")

    elif request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        image_url = request.form['image_url']

        print('here are the variables', first_name, last_name, image_url)

        if image_url == "":
            image_url = None 

        new_user =  User(first_name=first_name,last_name=last_name,image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect("/users")
    
@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Loads user profile page"""
    
    user = User.query.get_or_404(user_id)

    return render_template(
        "user_details.html",
        user = user
    )

@app.route('/users/<user_id>/edit', methods =['GET', 'POST'])
def user_edit(user_id):
    """Loads an edit user post form, with a cancel button that returns the user page, and a save button that edits the user page"""
    user = User.query.get_or_404(user_id)
    # og_img = user.image_url
    # og_first = user.first_name
    # og_last = user.last_name
    

    if request.method == 'GET':
        return render_template(
            'edit.html', 
            user = user
            )


    if request.method == 'POST':
        # user.first_name =  request.form['first_name']
        # user.last_name =  request.form['last_name']
        # user.image_url =  request.form['image_url']

        if request.form['first_name'] != "":
            user.first_name =request.form["first_name"]
        if request.form['last_name'] != "":
            user.last_name =request.form["last_name"]
        if request.form['image_url'] != "":
            user.image_url =request.form["image_url"]

        # if user.image_url == "":
        #     user.image_url = og_img
        # if user.first_name == "":
        #     user.first_name = og_first
        # if user.last_name == "":
        #     user.last_name = og_last

        db.session.commit()
        return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """Deletes our selected user, and redirects back to the /users page"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)

    db.session.commit()
    return redirect("/users")


    
    

