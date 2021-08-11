"""
We will store Database models into this python file.
    - Database Model for users
    - Database Model for storing the Notes
"""
from . import db # import the Database object created in the __init__.py file
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    data= db.Column(db.String(10000))
    date= db.Column(db.DateTime(timezone=True), default=func.now())
    user_id= db.Column(db.Integer, db.ForeignKey('user.id')) # setting a foreign key, to set up one-many relationship


# We will create a class which will contain all the columns that we want to store into our User database (Defining a Schema0
class User(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(150), unique=True)
    password= db.Column(db.String(150))
    first_name= db.Column(db.String(150))
    notes= db.relationship('Note') # Add note_id to user everytime we create a note

