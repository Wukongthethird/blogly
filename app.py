"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User, Post, Tag
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
    posts = user.posts

    return render_template(
        "user_details.html",
        user=user,
        posts=posts
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

        if request.form['first_name'] != "":
            user.first_name =request.form["first_name"]
        if request.form['last_name'] != "":
            user.last_name =request.form["last_name"]
        if request.form['image_url'] != "":
            user.image_url =request.form["image_url"]

        db.session.commit()
        return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    """Deletes our selected user, and redirects back to the /users page"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)

    db.session.commit()
    return redirect("/users")


@app.route('/users/<user_id>/posts/new', methods = ['GET', 'POST']) 
def add_post(user_id):
    """Accesses add post form, handles add post form, and redirects to user profile page""" 

    user = User.query.get(user_id)

    if request.method == 'GET':
        return render_template(
            'new_post.html', 
            user=user
            )

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        new_post= Post(title=title,content=content, user_id=user_id)

        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user.id}")

@app.route('/posts/<post_id>') 
def display_post(post_id):
    
    post = Post.query.get(post_id)
    

    return render_template(
        'display_posts.html',
        post=post,
        user=post.user
        )

@app.route('/posts/<post_id>/edit', methods = ['GET',"POST"]) 
def edit_post(post_id):
    
    post = Post.query.get(post_id)
    
    if request.method == 'GET':
        return render_template(
            'edit_post.html',
            post=post,
            user=post.user
            )

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        post.title = title
        post.content = content

        db.session.commit()
        return redirect(f"/posts/{post.id}")

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    """Deletes our selected user, and redirects back to the /users page"""

    post = Post.query.get_or_404(post_id)
    user_id = post.user.id


    db.session.delete(post)

    db.session.commit()
    return redirect(f"/users/{user_id}")



@app.route('/tags')
def load_tags():
    """Loads our homepage"""
    tags = Tag.query.all()
    return render_template(
        "tags.html",
        tags=tags
        )

@app.route('/tags/<tag_id>') 
def display_tag(tag_id):
    
    tag = Tag.query.get(tag_id)
    

    return render_template(
        'display_tag.html',
        tag=tag
        )


@app.route('/tags/new', methods = ['GET','POST'])
def load_new_tag():
    """Loads our homepage"""

    if request.method == "GET":

        return render_template(
            "new_tag.html"
        )

    elif request.method == "POST":

        tag_name = request.form['tag']

        new_tag= Tag(name=tag_name)

        db.session.add(new_tag)
        db.session.commit()
        return redirect("/tags")

@app.route('/tags/<tag_id>/edit', methods = ['GET',"POST"]) 
def edit_tag(tag_id):
    
    tag = Tag.query.get(tag_id)
    
    if request.method == 'GET':
        return render_template(
            'edit_tags.html',
            tag=tag,
            )

    if request.method == 'POST':
        name = request.form['name']

        tag.name = name

        db.session.commit()
        return redirect(f"/tags/{tag.id}")

@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    """Deletes our selected user, and redirects back to the /users page"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)

    db.session.commit()
    return redirect(f"/tags")


