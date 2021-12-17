from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

# CREATE a DB object 
# opening up the db connection 
DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key = True, nullable= False)
    username = DB.Column(DB.String, nullable= False)


class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key = True, nullable = False)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable = False)
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)
    vect = DB.Column(DB.PickleType, nullable=False)
