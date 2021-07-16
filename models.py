"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime


#todo global the image url
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"
    """Table Columns"""
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    
    first_name = db.Column(db.TEXT,
                            nullable=False
                        )
    last_name = db.Column(db.TEXT,
                            nullable=False
                        )
                            
    image_url =  db.Column(db.TEXT,
                            nullable=False,
                            default="https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/SpongeBob_SquarePants_character.svg/440px-SpongeBob_SquarePants_character.svg.png"
    )

    user_posts = db.relationship('Post',
                                backref='user', lazy='joined')
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    
class Post(db.Model):
    """Post"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
            
    title = db.Column(db.TEXT,
                            nullable=False)
                            
    content = db.Column(db.TEXT,
                            nullable=False)

    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default=datetime.datetime.utcnow)

    user_id = db.Column(db.ForeignKey('users.id'),
                            nullable=False)    



                            

class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    




class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )

    



