"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app):
  db.app = app
  db.init_app(app)




class Users(db.Model):
  """users table"""

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key = True, autoincrement=True)
  first_name = db.Column(db.String, nullable=False)
  last_name = db.Column(db.String, nullable=False)
  img_url = db.Column(db.String, nullable=False, default="https://i.stack.imgur.com/34AD2.jpg")

class Posts(db.Model):
  """Blogly posts table"""

  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key = True, autoincrement=True)
  title = db.Column(db.String, nullable=False)
  content = db.Column(db.String, nullable=False)
  created_on = db.Column(db.DateTime, server_default=db.func.now())
  auth_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

  author = db.relationship('Users', backref=backref('posts', cascade='all, delete-orphan'))
  tags = db.relationship('Tag', secondary='post_tags', backref='posts')

class Tag(db.Model):
  """article tags table"""

  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String, nullable=False)

class PostTag(db.Model):
  """post tag relationship table"""

  __tablename__ = 'post_tags'

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
