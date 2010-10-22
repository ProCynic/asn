"""
"""

import re
from datastore import *

def _addPerson(fname,lname, mname=None):
    """
    """
    #if person in datastore:
        #return person.key()
    p = Person(fname=fname,
               lname=lname,
               mname=mname)
    p.put()
    return p.key()

def addBook(title,isbn,author):
    """
    """
    isbn = isbn.strip().replace('-','')
    #pull out fname, lname, mname from author

    a = _addPerson(afname,alname,amname)
    b = Book(title=title,
             isbn=isbn,
             author=a)

def addCourse(unique, courseNum, name, semester, instructor, grade):
    """
    """
    #regexps to pull out data
    i = _addPerson(fname, lname, mname)
    c = Course(unique=unique,
               courseNum=courseNum,
               name=name,
               semester=semester,
               year=year,
               grade=grade,
               instructor=i)
    c.put()
    return c.key()

    
def addRating(ratable, student, rating, comment=None):
    """
    """
    r = Rating(rated=ratable,
               rater=student,
               rating=rating,
               comment=comment)
    r.put()
    return r.key()
