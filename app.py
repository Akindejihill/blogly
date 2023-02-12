
"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db, getJoin, User, Post, PostTag, Tag, make_db, seed_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly' #use this for production
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly-test' #use this for testing
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.config['SECRET_KEY'] = 'chickenzarcool21837'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def homepage():
    #This has more text and code than using a through relationship, but it only uses 2 queries, rather than a bagillion queries
    select = getJoin(fields = (*Post.all, User.first_name, User.last_name), joinTable=User).order_by(Post.created_at.desc()).limit(5).all()
    postIds = [postID[0] for postID in select]  #gather all the post ids from the selected posts
    #select all the tags from all the selected posts
    selectTags = getJoin(fields = (*PostTag.all, Tag.name), joinTable=Tag, filter=(PostTag.post_id.in_(postIds))).all() 

    #create a new list of posts with the correct tags appended to the associated post.
    posts = []
    for selection in select:
        post = {}
        post['id'] = selection.id
        post['title'] = selection.title
        post['content'] = selection.content
        post['created_at'] = selection.created_at
        post['author'] = selection.author
        post['first_name ']= selection.first_name
        post['last_name'] = selection.last_name
        #my first try resulted in a query for each loop.  That's no good.
        #post['tags'] = getJoin(fields = (*PostTag.all, Tag.name), joinTable=Tag, filter=(PostTag.post_id==selection.id)).all()

        #I added one query above this block to get all the tags for all the posts, now here we just need to arrange them by post.
        tags = []
        for tag in selectTags:
            if tag.post_id == selection.id:
                tags.append(tag)
        post['tags'] = tags
        posts.append(post)

    #for each post add a tuple of tags belonging to it
    return render_template('home.html', posts=posts)

@app.route('/users')
def list_users():
    """Shows Users"""
    users = User.query.all()
    return render_template('userlist.html', users=users)

@app.route('/users/new')
def show_form():
    """Show new users form"""
    return render_template('/add_user.html')


@app.route('/users/new', methods = ['POST'])
def adduser_form():
    """Adds new user and redirects back"""
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
    """Shows a Post"""
    #The M2M relationship of the commented out select below works, but only does inner join.  Excludes posts with no tags
    #select = getJoin(fields=(Tag.id, Tag.name, PostTag.post_id, Post.title, Post.content, Post.created_at, Post.author ,User.first_name, User.last_name), fromTable=Tag, joinTable=PostTag, joinTable2=Post, joinTable3=User, filter=(Post.id==post_id)).all()
    #Solution: get the tags in a separate query
    select = getJoin(fields=(Post.id, Post.title, Post.content, Post.created_at, Post.author ,User.first_name, User.last_name), fromTable=Post, joinTable=User, filter=(Post.id==post_id)).all()
    tags = getJoin(fields=(PostTag, Tag), joinTable=Tag, filter=(PostTag.post_id==post_id)).all()
    if len(select):
        return render_template('showpost.html', select=select, tags=tags)
    else:
        return "Post was not found"


@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """displays a form to add a post for this user"""

    usr = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template('new_post.html', user=user_id, firstname=usr.first_name, lastname=usr.last_name, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def add_new_post(user_id):
    """ Adds a new post to the database """
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags')

    newPostID = Post.add(ptitle=title, pcontent=content, pauthor=user_id)
    PostTag.add(tags, newPostID)

    return redirect(f'/users/{user_id}') 


@app.route('/posts/<int:postid>/edit')
def show_editpost_form(postid):
    """displays a form to edit a post"""
    tags = Tag.query.all()
    post = getJoin(fields=(*Post.all, User.first_name, User.last_name), joinTable=User, filter=(Post.id==postid)).first()
    tagged = db.session.query(PostTag.tag_id).filter_by(post_id = postid).all()
    checked=[] #get the tag ids into a friendly list format
    for tag in tagged:
        checked.append(tag[0])
    return render_template('edit_post.html', post=post, tags=tags, checked=checked)

@app.route('/posts/<int:post_id>/edit', methods = ['POST'])
def edit_post(post_id):
    """update a post in the database"""
    
    Post.edit_post(post_id, request=request)
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete a post"""
    post = Post.query.get(post_id)
    uid = post.author
    Post.delete_post(post_id)
    return redirect(f'/users/{uid}')

@app.route('/tags')
def show_all_tags():
    """Display all the tags"""
    tags = Tag.query.all()
    return render_template('show_all_tags.html', tags=tags)

@app.route('/tags/<int:tagID>')
def show_tag(tagID):
    """ Show tag page """
    select = getJoin(fields = (Tag.id, Tag.name, PostTag.post_id, Post.title),fromTable=Tag, joinTable=PostTag, joinTable2=Post, filter=(Tag.id == tagID)).order_by(Post.created_at.desc()).limit(5).all()
    if len(select):
        return render_template('tag.html', select=select)
    else:
        select=Tag.query.filter_by(id = tagID).all()
        return render_template('tag.html', select=select)


@app.route('/tags/new')
def new_tag_form():
    """Show the form for creating a new tag"""
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def new_tag():
    """ Add a new tag to the database  """
    tag = request.form['tag']
    Tag.add(tag)
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Delete a tag"""
    result = Tag.delete(tag_id)
    if result:
        return redirect('/tags')
    else:
        return "<html><body><h1>Delete failed for some reason</h1><h2>Make sure tag is not assigned to any posts</h2></body></html>"

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Show form to edit a tag"""
    tag=Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods = ['POST'])
def edit_tag(tag_id):
    """Submit Tag Edit to database"""
    Tag.edit(tag_id, request)
    return redirect('/tags')

