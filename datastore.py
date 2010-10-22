"""
"""

from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import users
from validators import *

class comment(db.Model):
    """
    """
    text = db.TextProperty(required=True)
    replyto = db.SelfReferenceProperty()

class person(db.model):
    fname = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    mname = db.StringProperty()

class student(db.model):
    info = db.ReferenceProperty(person, required=True)
    idNum = db.IntegerProperty(required=True)
    password = db.StringProperty(required=True)

class ratable(polymodel.PolyModel):
    """
    """
    pass

class rating(db.Model):
    """
    """
    rating = db.RatingProperty(required=True)
    comment = db.ReferenceProperty(comment)
    rated = db.ReferenceProperty(ratable)
    rater = db.ReferenceProperty(student)

class course (ratable):
    """
    """
    unique = db.StringProperty(required=True,validator=uniqueValidator)
    courseNum = db.StringProperty(required=True, validator=courseNumValidator)
    name = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    instructor = db.ReferenceProperty(person, required=True)
    grade = db.StringProperty(required=True, validator=gradeValidator)
    year = db.StringProperty(required=True, validator=yearValidator)



class book(ratable):
    """
    """
    isbn = db.StringProperty()
    title = db.StringProperty()
    author = db.ReferenceProperty(person)

class paper(ratable):
    """
    """
    journal = db.StringProperty()
    title = db.StringProperty()
    author = db.ReferenceProperty(person)

class place (ratable):
    """
    """
    name = db.StringProperty()
    location = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    year = db.StringProperty(validator=yearValidator)
    latLong = db.GeoPtProperty()

class internship (place):
    """
    """
    company = db.StringProperty(required=True)
    location = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    year = db.StringProperty(validator=yearValidator)

class placeLive (place):
    """
    """
    pass

class placeEat (place):
    """
    """
    pass

class placeFun (place):
    """
    """
    pass

class placeStudy (place):
    """
    """
    pass

class game (ratable):
    """
    """
    platform = db.StringProperty(required=True,choices=gamePlatforms)
    title = db.StringProperty(required=True)

gamePlatforms = [
    "XBOX",
    "XBOX 360",
    "PLAYSTATION",
    "PLAYSTATION 2",
    "PLAYSTATION 3",
    "NINTINDO",
    "SUPER NINTINDO",
    "NINTINDO 64",
    "GAMECUBE",
    "WII",
    "SEGA GENISIS",
    "PC",
    "MAC",
    "LINUX",
    "GAMEBOY",
    "NINTINDO DS",
    "PSP",
    "IPHONE",
    "ANDROID",
    "CELLPHONE"]
