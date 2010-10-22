"""
"""

import re
from datastore import *

def _addPerson(name):
    """
    """

    name = name.split()
    if len(name) not in [2, 3]:
    	raise ValueError
    fname = name[0]
    if len(name) > 2:
    	mname = name[1]
    	lname = name[2]
    else :
    	mname = None
    	lname = name[1]
    #if person in datastore:
        #return person.key()
    query = Person.all()
   	query.filter('fname =', fname).filter('mname =', mname).filter('lname =', lname)
    results = query.fetch()
    if len(results) > 1: raise Exception
    if len(results) == 1: return results.get().key()
    p = Person(fname=fname,
       lname=lname,
       mname=mname)
    p.put()
    return p.key()

def addBook(title,isbn,author):
    """
    """
    isbn = isbn.strip().replace('-','')
    
    a = _addPerson(author)
    b = Book(title=title,
             isbn=isbn,
             author=a)

def addCourse(unique, courseNum, name, semester, year, instructor, grade):
    """
    """
    i = _addPerson(instructor)
    c = Course(unique=unique,
               courseNum=courseNum,
               name=name,
               semester=semester,
               year=year,
               grade=grade,
               instructor=i)
    c.put()
    return c.key()

def addPaper(journal, title, author):
    fname,lname,mname = parseName(author)
    a = _addPerson(author)
    p = Paper(journal=journal,
              title=title,
              author=a)

def addPlace(name, location, semester, year, placetype):
    p = placetype(name=name,
                  location=location,
                  semester=semester,
                  year=year)
    return p.key()

def addPlaceLive(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceLive)


def addRating(ratable, student, rating, comment=None):
    """
    """
    r = Rating(rated=ratable,
               rater=student,
               rating=rating,
               comment=comment)
    r.put()

    return r.key()

