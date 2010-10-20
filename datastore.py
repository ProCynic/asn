"""
"""

import re
from google.appengine.ext import db
from google.appengine.api import users

class ratable(db.model):
    #member vars
    pass

class course (ratable):
    unique = db.StringProperty(required=True,validator=uniqueValidator)
    courseNum = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    semeseter = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])

class place (ratable):
    location = db.StringProperty(required=True)
    semeseter = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])

class internship (place):
    company = db.StringProperty(required=True)

class placeLive (place):
    pass

class placeEat (ratable):
    pass

class placeFun (ratable):
    pass

class game (ratable):
    platform = db.StringProperty(required=True)
    title = db.StringProperty(required=True)

class comment(db.model):
    text = db.Text()


def uniqueValidator(value):
    unique = re.search("^\d{5}$",value)
    if unique is None: raise ValueError
