
"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import connect_db, User, Post, make_db, seed_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = 'chickenzarcool21837'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def homepage():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('home.html', posts=posts)

@app.route('/users')
def list_users():
    """Shows Users"""
    users = User.query.all()
    return render_template('userlist.html', users=users)

@app.route('/users/new')
def show_form():
    return render_template('/add_user.html')


@app.route('/users/new', methods = ['POST'])
def adduser_form():
    """Shows add user form"""
    firstn=request.form['firstname']
    lastn=request.form['lastname']
    img=request.form['imgurl']

    User.add(firstn, lastn, img)
    return redirect("/", code=302)


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Shows user information"""
    user = User.query.filter_by(id = user_id).first()
    posts = Post.query.filter_by(author = user_id).all()
    return render_template('showuser.html', user = user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    """Show edit form"""
    user = User.query.filter_by(id = user_id).first()
    return render_template('edituser.html', user = user)


@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    User.edit_user(user_id, request)
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete')
def delete(user_id):
    User.delete_user(user_id)
    return redirect('/users')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('showpost.html', post=post)



@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """displays a form to add a post for this user"""

    usr = User.query.get(user_id)
    return render_template('new_post.html', user=user_id, firstname=usr.first_name, lastname=usr.last_name)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def add_new_post(user_id):
    """displays a form to add a post for this user"""
    title = request.form['title']
    content = request.form['content']

    Post.add(ptitle=title, pcontent=content, pauthor=user_id)
    return redirect(f'/users/{user_id}') 


@app.route('/posts/<int:post_id>/edit')
def show_editpost_form(post_id):
    """displays a form to edit a post"""
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def edit_post(post_id):
    """update a post in the database"""
    
    Post.edit_post(post_id=post_id, request=request)
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get(post_id)
    uid = post.user.id
    Post.delete_post(post_id)
    return redirect(f'/users/{uid}')
