"""
"""

from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import users
from validators import *

class comment(db.Model):
    """
    """
    text = db.TextProperty()
    replyto = SelfReferenceProperty()

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

class course (ratable):
    """
    """
    unique = db.StringProperty(required=True,validator=uniqueValidator)
    courseNum = db.StringProperty(required=True, validator=courseNumValidator)
    name = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    instructor = db.StringProperty(required=True, validator=personNameValidator)
    grade = db.StringProperty(required=True, validator=gradeValidator)
    year = db.StringProperty(requierd=True, validator=yearValidator)



class book(ratable):
    """
    """
    isbn = db.StringProperty(validator=isbnValidator)
    title = db.StringProperty()
    author = db.StringProperty(validator=personNameValidator)

class paper(ratable):
    """
    """
    journal = db.StringProperty()
    title = db.StringProperty()
    author = db.StringProperty(validator=personNameValidator)


class place (ratable):
    """
    """
    location = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    year = db.StringProperty(validator=yearValidator)
    latLong = db.GeoPtProperty()

class internship (place):
    """
    """
    company = db.StringProperty(required=True)

class placeLive (place):
    """
    """
    pass

class placeEat (ratable):
    """
    """
    pass

class placeFun (ratable):
    """
    """
    pass

class game (ratable):
    """
    """
    platform = db.StringProperty(required=True)
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
    "PC",
    "MAC",
    "LINUX",
    "GAMEBOY",
    "NINTINDO DS",
    "PSP",
    "IPHONE",
    "ANDROID",
    "CELLPHONE"]
