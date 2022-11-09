"""Models for Blogly."""

# from datetime import datetime
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""
    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id}, first_name={u.first_name}, last_name={u.last_name}, image_url={u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String, nullable=False,
                          default='https://thumbs.dreamstime.com/b/woman-natural-beauty-makeup-portrait-fashion-model-touching-face-hands-beautiful-girl-skin-care-treatment-woman-natural-140288618.jpg')


class Post(db.Model):
    """ User posts"""
    __tablename__ = 'posts'

    def __repr__(self):
        p = self
        return f"<Post id={p.id}, title=p.title, content=p.content>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='posts')
