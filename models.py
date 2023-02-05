"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
        return f"Hi dickhead!  My name is {self.first_name} {self.last_name}.  Now, fuck off!"

    @classmethod
    def add(self, first, last, url):
        user0 = User(first_name = first, last_name = last, image_url = url)
        db.session.add(user0)
        db.session.commit()

    
    @classmethod
    def edituser(self, user_id, request):
        user = User.query.get(user_id)
        user.first_name = request.form["firstname"]
        user.last_name = request.form["lastnames"]
        user.image_url = request.form["imgurl"]
        db.session.commit()

    @classmethod
    def delete_user(self, user_id):
        User.query.filter_by(id = user_id).delete()
        db.session.commit()

    


def make_db():
    db.create_all()

def seed_db():
    user1 = User(first_name = "Alen", last_name = "Alda")
    user2 = User(first_name = "Joel", last_name = "Burton")
    user3 = User(first_name = "Jane", last_name = "Smith")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    db.session.commit()

