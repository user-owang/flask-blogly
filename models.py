"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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