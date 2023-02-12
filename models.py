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
        user.last_name = request.form["lastname"]
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

    #replaced through relationship with multi join queries
    #tags = db.relationship('Tag', secondary='post_tags', backref='posts')

    #replaced relationship with explicite join
    #user = db.relationship('User')

    #Class variable
    all = (id, title, content, created_at, author)

    @classmethod
    def add(self, ptitle, pcontent, pauthor):
        """Adds a new post to database and returns its id """
        post0 = Post(title = ptitle, content = pcontent, author = pauthor)
        db.session.add(post0)
        db.session.commit()
        return post0.id

    @classmethod
    def edit_post(self, postid, request):
        """Updates a post and its tags in the database"""
        post = Post.query.get(postid)
        post.title = request.form['title']
        post.content = request.form['content']
        tags=request.form.getlist('tags')
        #Delete all post tag associations
        print("\n\n\n Deleting Tags \n\n\n")
        PostTag.query.filter_by(post_id = postid).delete()
        db.session.commit
        #Insert the new post tag associations
        print("\n\n\n Inserting Tags \n\n\n")
        for tag in tags:
            tag0 = PostTag(post_id = postid, tag_id = tag)
            db.session.add(tag0)
        db.session.commit()
        


    @classmethod
    def delete_post(self, postid):
        """Delete's a post and it's tags in the database"""
        PostTag.query.filter_by(post_id = postid).delete()
        db.session.commit() #ensure that post tag associations are deleted first
        Post.query.filter_by(id = postid).delete()
        db.session.commit()


class PostTag(db.Model):
    __tablename__ = 'post_tags'

    def __repr__(self) -> str:
        return f"Association table for post and tags\nPostID: {self.post_id}\nTagId: {self.tag_id}"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable = False, primary_key=True)
    
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable = False, primary_key=True)

    #Class variable
    all = (post_id, tag_id)

    @classmethod
    def add(self, tags, post):
        for tag in tags:
            tag = PostTag(post_id = post, tag_id = tag)
            db.session.add(tag)
        db.session.commit()


class Tag(db.Model):
    __tablename__ = 'tags'

    def __repr__(self):
        return f"Tag id: {self.id}\nName: {self.name}"

    id = db.Column(db.Integer, nullable = False, primary_key=True, autoincrement=True)
    
    name = db.Column(db.String(15), nullable = False, unique = True)

    @classmethod
    def add(self, tag):
        """Adds a new tag to database"""
        tag0 = Tag(name = tag)
        db.session.add(tag0)
        db.session.commit()

    @classmethod
    def delete(self, tag_id):
        """Delete a tag from database"""
        try:
            Tag.query.filter_by(id = tag_id).delete()
            db.session.commit()
        except:
            return False
        return True

    @classmethod
    def edit(self, tag_id, request):
        tag = Tag.query.get(tag_id)
        tag.name = request.form['name']
        db.session.commit()


def getJoin(fields, joinTable, fromTable=None, joinTable2 = "nothing", joinTable3 = "nothing", filter = "nothing"):
    """Sends back a table with the fields and records requested from two inner-joined tables
        Takes field, joinTable, filter(optional)
        fields - an iterable containing selected fields form two tables. Use *Post.all for all fields
        fromTable - The left table, required for more than one join
        joinTable - the table with the inner join
        filter - Where clauses, required to get specific record(s)
        *Note you can't use .get or .first with this return value
        *You must select and filter the records you want using this method's
        *filter argument (i.e. Post.id == 1).  
        *You can attach other modifiers like .order_by .limit and .all
    """
    if joinTable2 == "nothing":
        if filter == "nothing":
            print("\n\n\n\nNot using where clause")
            print(f"Filter: {filter}\n\n\n\n" )
            return db.session.query(*fields).outerjoin(joinTable)
        else:
            print("\n\n\n\nUsing filter\n\n\n\n")
            return db.session.query(*fields).outerjoin(joinTable).filter(filter)

    else:
        if joinTable3 == "nothing":
            if filter == "nothing":
                print("\n\n\n\nNot using where clause")
                print(f"Filter: {filter}\n\n\n\n" )
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2)
            else:
                print("\n\n\n\nUsing filter\n\n\n\n")
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2).filter(filter)
        else:
            if filter == "nothing":
                print("\n\n\n\nNot using where clause")
                print(f"Filter: {filter}\n\n\n\n" )
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2).join(joinTable3)
            else:
                print("\n\n\n\nUsing filter\n\n\n\n")
                return db.session.query(*fields).select_from(fromTable).outerjoin(joinTable).join(joinTable2).join(joinTable3).filter(filter)


    




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
    
    db.session.commit()

    post1 = Post(title = "Post 1 title", content = "post 1 content blah blah blah", author = 1)
    post2 = Post(title = "Post 2 title!", content = "post 2 content blah blah blah", author = 2)
    post3 = Post(title = "Post 3 title?", content = "post 3 content blah blah blah", author = 3)
    post4 = Post(title = "Post 4 title", content = "post 4 content blah blah blah", author = 1)
    post5 = Post(title = "Post 5 title!", content = "post 5 content blah blah blah", author = 2)
    post6 = Post(title = "Post 6 title?", content = "post 6 content blah blah blah", author = 3)


    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
    db.session.add(post5)
    db.session.add(post6)
    
    db.session.commit()

    tag1 = Tag(name = 'first post')
    tag2 = Tag(name = "second post")
    tag3 = Tag(name = "third post")
    tag4 = Tag(name = 'Test tag')

    db.session.add_all([tag1, tag2, tag3, tag4])
    db.session.commit()

    posttag1 = PostTag(post_id = 1, tag_id = 1)
    posttag2 = PostTag(post_id = 2, tag_id = 2)
    posttag3 = PostTag(post_id = 3, tag_id = 3)
    posttag4 = PostTag(post_id = 1, tag_id = 4)
    posttag5 = PostTag(post_id = 2, tag_id = 4)
    posttag6 = PostTag(post_id = 3, tag_id = 4)
    posttag7 = PostTag(post_id = 4, tag_id = 4)
    posttag8 = PostTag(post_id = 5, tag_id = 4)
    posttag9 = PostTag(post_id = 6, tag_id = 4)

    db.session.add_all([posttag1, posttag2, posttag3, posttag4, posttag5, posttag6, posttag7, posttag8, posttag9])
    db.session.commit()

