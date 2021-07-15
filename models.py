"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
    

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    


