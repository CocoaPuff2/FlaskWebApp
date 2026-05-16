# create db models 
from . import db #importing from current package (website folder)
from flask_login import UserMixin # custom class 
from sqlalchemy.sql import func

# db model for users
class User(db.Model, UserMixin):
    # define columns stored in this table (schema/layout)
    # primary key for all objects (unique id per user)
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    # tell flask and sql that every time note created,
    #  add that note id to this list 
    note = db.relationship('Note')
    

# db model for notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    #f foreign key = references an id to another db column 
    # store the id of the user who created the note
    # must pass valid id of existing user when creating a new note (one-to-many)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))