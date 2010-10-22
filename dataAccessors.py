"""
"""

import re
from datastore import *

def _addPerson(name):
    """
    """
    name = name.strip.split();
    if len(name) == 2: fname, lname, mname = name, None
    else if len(name) == 3: fname, mname, lname = name
    else raise ValueError
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
    isbn = int(isbn.strip().replace('-',''))
    
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

def _addPlace(name, location, semester, year, placetype):
    """
    """
    #might be cool to translate address into latlong
    p = placetype(name=name,
                  location=location,
                  semester=semester,
                  year=year)
    return p.key()

def addPlaceLive(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceLive)

def addPlaceEat(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceLive)

def addPlaceFun(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceLive)

def addPlaceStudy(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceLive)

def addInternship(company, location, semester, year):
    """
    """
    i = Internship(company=company,
                   location=location,
                   semseter=semester,
                   year=year)
    i.put()
    return i.key()

def addGame(platform, title):
    """
    """
    g = Game(platform=platform,
             title=title)
    g.put()
    return g.key()

def addRating(ratable, student, rating, comment=None):
    """
    """
    r = Rating(rated=ratable,
               rater=student,
               rating=rating,
               comment=comment)
    r.put()
    return r.key()
    
