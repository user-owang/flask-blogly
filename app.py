"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Posts, Tag, PostTag

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def show_home():
  return redirect('/users')

@app.route('/users')
def list_users():
  """list of all users in table"""
  users = Users.query.all()
  return render_template('users.html', users=users)

@app.route('/users/new')
def show_user_form():
  """Show form to add new user"""
  return render_template('newuser.html')

@app.route('/users/new', methods=['POST'])
def create_new_user():
  """Logic to add new user to table"""
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  img_url = request.form['img_url']

  if img_url != '':
    new_user = Users(first_name=first_name, last_name=last_name, img_url=img_url)
  else:
    new_user = Users(first_name=first_name, last_name=last_name)
  db.session.add(new_user)
  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
  """display details of a single user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
  """show form to edit detials of a single user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  return render_template('edituser.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
  """logic to edit details of a single user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  if request.form['img_url']:
    user.img_url = request.form['img_url']

  db.session.add(user)
  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
  """logic to delete a single user with user.id == user_id from the table"""
  Users.query.filter_by(id=user_id).delete()

  db.session.commit()
  return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
  """show form to add a new post as user with user.id == user_id"""
  user = Users.query.get_or_404(user_id)
  tags = Tag.query.all()
  return render_template('newpost.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
  """logic to add a new post to table as a user with user.id == user_id"""
  title = request.form['title']
  content = request.form['content']
  user = Users.query.get_or_404(user_id)
  new_post = Posts(title=title, content=content, auth_id=user.id)
  post_tags = request.form.getlist('tags')
  for tag in post_tags:
    new_post_tag = Tag.query.get(int(tag))
    new_post.tags.append(new_post_tag)

  db.session.add(new_post)
  db.session.commit()
  return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
  """Show post details where post.id == post_id"""
  post = Posts.query.get_or_404(post_id)
  return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
  """Show form to edit post where post.id == post_id"""
  post = Posts.query.get_or_404(post_id)
  tags = Tag.query.all()
  return render_template('editpost.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
  """logic to edit post and update table where post.id == post_id"""
  post = Posts.query.get_or_404(post_id)
  post.title = request.form['title']
  post.content = request.form['content']
  post.tags = []
  post_tags = request.form.getlist('tags')
  for tag in post_tags:
    new_post_tag = Tag.query.get(int(tag))
    post.tags.append(new_post_tag)

  db.session.add(post)
  db.session.commit()
  return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
  """logic to delete a post with post.id == post_id from the table"""
  post = Posts.query.get_or_404(post_id)
  auth = post.auth_id
  Posts.query.filter_by(id=post_id).delete()

  db.session.commit()
  return redirect(f'/users/{auth}')

@app.route('/tags')
def show_tags():
  """shows a list of all tags"""
  tags = Tag.query.all()

  return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
  """shows details for a tag with tag.id == tag_id"""
  tag = Tag.query.get_or_404(tag_id)

  return render_template('tagdetails.html', tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
  """shows form to add a new tag"""
  return render_template('newtag.html')

@app.route('/tags/new', methods = ['POST'])
def add_new_tag():
  """logic to add new tag to table"""
  name = request.form['name']
  new_tag = Tag(name=name)

  db.session.add(new_tag)
  db.session.commit()
  return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
  """show form to edit a tag with tag.id == tag_id"""
  tag = Tag.query.get_or_404(tag_id)
  return render_template('edittag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def edit_tag(tag_id):
  """logic to edit a tag with tag.id == tag_id"""
  tag = Tag.query.get_or_404(tag_id)
  tag.name = request.form('name')

  db.session.add(tag)
  db.session.commit()
  return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
  """logic to delete tag with tag.id = tag_id"""
  Tag.query.filter_by(id=tag_id).delete()

  db.session.commit()
  return redirect('/tags')