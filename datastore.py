"""
"""

from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from validators import *

class Comment(db.Model):
    """
    """
    text = db.TextProperty(required=True)
    replyto = db.SelfReferenceProperty()

class Person(db.model):
    fname = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    mname = db.StringProperty()

class Student(db.model):
    info = db.ReferenceProperty(person, required=True)
    sid = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

class Ratable(polymodel.PolyModel):
    """
    """
    pass

class Rating(db.Model):
    """
    """
    rating = db.RatingProperty(required=True)
    comment = db.ReferenceProperty(comment)
    rated = db.ReferenceProperty(ratable)
    rater = db.ReferenceProperty(student)

class Course (ratable):
    """
    """
    unique = db.StringProperty(required=True,validator=uniqueValidator)
    courseNum = db.StringProperty(required=True, validator=courseNumValidator)
    name = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    instructor = db.ReferenceProperty(person, required=True)
    grade = db.StringProperty(required=True, validator=gradeValidator)
    year = db.StringProperty(required=True, validator=yearValidator)



class Book(ratable):
    """
    """
    isbn = db.StringProperty()
    title = db.StringProperty()
    author = db.ReferenceProperty(person)

class Paper(ratable):
    """
    """
    journal = db.StringProperty()
    title = db.StringProperty()
    author = db.ReferenceProperty(person)

class Place (ratable):
    """
    """
    name = db.StringProperty()
    location = db.PostalAddressProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    year = db.StringProperty(validator=yearValidator)
    latLong = db.GeoPtProperty()

class Internship (place):
    """
    """
    company = db.StringProperty(required=True)
    location = db.PostalAddressProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    year = db.StringProperty(validator=yearValidator)

class PlaceLive (place):
    """
    """
    pass

class PlaceEat (place):
    """
    """
    pass

class PlaceFun (place):
    """
    """
    pass

class PlaceStudy (place):
    """
    """
    pass

class Game (ratable):
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
