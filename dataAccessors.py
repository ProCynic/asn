"""
"""

import re
from datastore import *

class datastoreController:
    """
    """
    __init__(self):
        pass

    def addPerson(fname,lname, mname=None):
        #if person in datastore:
            #return person.key()
        p = Person(fname=fname,
                   lname=lname,
                   mname=mname)
        p.put()
        return p.key()

    def addBook(title,isbn,author):
        isbn = isbn.strip().replace('-','')
        #pull out fname, lname, mname from author

        a = _addPerson(afname,alname,amname)
        b = Book(title=title,
                 isbn=isbn,
                 author=a)

    def addCourse(unique, courseNum, name, semester, instructor, grade):
        #regexps to pull out data
        i = _addPerson(fname, lname, mname)
        
    def addRating(rating, ratable, comment=None):
        r = 
