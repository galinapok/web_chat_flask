from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from myapp.database import Base
from sqlalchemy.orm import relationship, backref
import datetime
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120), unique=False)
    user_image_file = Column(String(120), unique=False)
    gender = Column(String(7), unique=False)
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name=None, email=None, password=None,  user_image_file= None, gender=None ):
        self.name = name
        self.email = email
        self.password = password
        self. user_image_file = user_image_file
        self.gender = gender
    def __repr__(self):
        return '<User %r>' % (self.name)

class Room (Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)    
    name = Column(String(50), unique=True)
   

    def __init__(self, name=None):
        self.name = name
       
    def __repr__(self):
        return '<Room %r>' % (self.name)




class Message (Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('rooms.id', onupdate="CASCADE", ondelete="CASCADE"))
    message = Column(String(50), unique=False)
    athor =Column(String(50), unique=False)
    pub_date = Column(DateTime)

    def __init__(self, parent_id=None,  message=None, athor=None, pub_date = None):
        self.parent_id = parent_id
        self.message = message
        self.athor = athor
        if pub_date is None:
            pub_date = datetime.datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Message %r>' % (self.message)
