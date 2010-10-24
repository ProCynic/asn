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

class Person(db.Model):
    fname = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    mname = db.StringProperty()

class Student(db.Model):
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
    comment = db.ReferenceProperty(Comment)
    rated = db.ReferenceProperty(Ratable)
    rater = db.ReferenceProperty(Student)

class Course (Ratable):
    """
    """
    unique = db.StringProperty(required=True,validator=uniqueValidator)
    courseNum = db.StringProperty(required=True, validator=courseNumValidator)
    name = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    instructor = db.ReferenceProperty(Person, required=True)
    year = db.StringProperty(required=True, validator=yearValidator)

class Grade(db.Model):
    """
    """
    course = db.ReferenceProperty(Course)
    student = db.ReferenceProperty(Student)
    grade = db.StringProperty(required=True, validator=gradeValidator)

class Book(Ratable):
    """
    """
    isbn = db.StringProperty()
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(Person,required=True)

class Paper(Ratable):
    """
    """
    paperType = db.StringProperty(required=True,choices=['JOURNAL','CONFERENCE'])
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(Person,required=True)

class Place (Ratable):
    """
    """
    name = db.StringProperty(required=True)
    location = db.PostalAddressProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    year = db.StringProperty(required=True,validator=yearValidator)
    latLong = db.GeoPtProperty()

class Internship (Place):
    """
    """
    pass

class PlaceLive (Place):
    """
    """
    pass

class PlaceEat (Place):
    """
    """
    pass

class PlaceFun (Place):
    """
    """
    pass

class PlaceStudy (Place):
    """
    """
    pass

class Game (Ratable):
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
