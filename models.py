"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    def __repr__(self):
        return f"<user id={self.id} first name={self.first_name} last name={self.last_name}>"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    first_name = db.Column(db.String(31),
                        nullable = False)

    last_name = db.Column(db.String(31))

    image_url = db.Column(db.String(2047),
                        default = "https://blogs.nottingham.ac.uk/learningtechnology/files/2022/01/aanonymouslong.jpg")
                    
        

    def greet(self):
        return f"Hi My name is {self.first_name} {self.last_name}."

    @classmethod
    def add(self, first, last, url):
        user0 = User(first_name = first, last_name = last, image_url = url)
        db.session.add(user0)
        db.session.commit()

    
    @classmethod
    def edit_user(self, user_id, request):
        user = User.query.get(user_id)
        user.first_name = request.form["firstname"]
        user.last_name = request.form["lastnames"]
        user.image_url = request.form["imgurl"]
        db.session.commit()

    @classmethod
    def delete_user(self, user_id):
        User.query.filter_by(id = user_id).delete()
        db.session.commit()



class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self) -> str:
        return f"post id: {self.id}, title: {self.title}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    title = db.Column(db.String(31),
                        nullable = False)
    
    content = db.Column(db.Text,
                        nullable = False)

    created_at = db.Column(db.DateTime,
                            nullable=False,
                            default = datetime.datetime.now)

    author = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')


    @classmethod
    def add(self, ptitle, pcontent, pauthor):
        post0 = Post(title = ptitle, content = pcontent, author = pauthor)
        db.session.add(post0)
        db.session.commit()


    @classmethod
    def edit_post(self, post_id, request):
        post = Post.query.get(post_id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()

    @classmethod
    def delete_post(self, post_id):
        Post.query.filter_by(id = post_id).delete()
        db.session.commit()


def make_db():
    db.drop_all()
    db.create_all()

def seed_db():
    user1 = User(first_name = "Alen", last_name = "Alda")
    user2 = User(first_name = "Joel", last_name = "Burton")
    user3 = User(first_name = "Jane", last_name = "Smith")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    post1 = Post(title = "Post 1 title", content = "post 1 content blah blah blah", author = 1)
    post2 = Post(title = "Post 2 title!", content = "post 2 content blah blah blah", author = 2)
    post3 = Post(title = "Post 3 title?", content = "post 3 content blah blah blah", author = 3)

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)

    db.session.commit()

