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
    


class comment(db.model):
    text = db.Text()


def uniqueValidator(value):
    unique = re.search("\d{5}")
    if unique is None: raise ValueError
