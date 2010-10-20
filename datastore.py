"""
"""

from google.appengine.ext import db
from db import polymodel
from google.appengine.api import users
from validators import *

class ratable(polymodel.PolyModel):
    """
    """
    pass

class rating(db.model):
    """
    """
    rating = db.Rating(required=True)
    comment = db.Text()
    rated = db.ReferenceProperty(ratable)

class course (ratable):
    """
    """
    unique = db.StringProperty(required=True,validator=uniqueValidator)
    courseNum = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    instructor = db.StringProperty(required=True)
    grade = db.StringProperty(required=True)
    year = db.StringProperty(requierd=True)

class book(ratable):
    """
    """
    isbn = db.StringProperty(required=True)
    title = db.StringProperty()
    author = db.StringProperty()

class paper(ratable):
    """
    """
    journal = db.StringProperty()
    title = db.StringProperty()
    author = db.StringProperty()


class place (ratable):
    """
    """
    location = db.StringProperty(required=True)
    semeseter = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])

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

class comment(db.model):
    """
    """
    text = db.Text()
