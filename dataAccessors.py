"""
"""

import re
from dataStore import *

class Usage (Exception):
    def __init__(self,msg):
        self.msg = msg

def _addPerson(name):
    """
    """

    name = name.strip().split()
    mname = None
    if len(name) == 2: fname, lname = name
    elif len(name) == 3: fname, mname, lname = name
    else: raise ValueError

    try:
        return checkMembership(Person,fname=fname, mname=mname, lname=lname)
    except KeyError:
        p = Person(fname=fname,
           lname=lname,
           mname=mname)
        p.put()
        return p.key()

def addStudent(sid, password):
    try:
        checkMembership(Student, sid=sid)
        raise Usage("Duplicate Student IDs")
    except KeyError, e:
        s = Student(sid=sid,
                    password=password)
        s.put()
        return s.key()

def addBook(title,isbn,author):
    """
    """
    try:
        return checkMembership(Book, isbn=isbn)
    except KeyError:
        isbn = isbn.strip().replace('-','')
        
        a = _addPerson(author)
        b = Book(title=title,
                 isbn=isbn,
                 author=a)
        b.put()
        return b.key()

def addCourse(unique, courseNum, name, semester, year, instructor):
    """
    """
    try:
        return checkMembership(Course, unique=unique)
    except KeyError:
        i = _addPerson(instructor)
        c = Course(unique=unique,
        		courseNum=courseNum,
        		name=name,
        		semester=semester,
        		year=year,
        		instructor=i)
    c.put()
    return c.key()

def addGrade(course,student,grade):
    try:
        return checkMembership(Grade, course=course, student=student)
    except KeyError:
    	g = Grade(course=course,
        		student=student,
        		grade=grade)
    	g.put()
    	return g.key()

def addPaper(journal, title, author):
    a = _addPerson(author)
    journal = jorunal.lower() #Make any insert conform to the xml schema inputs.
    try:
        return checkMembership(Paper, journal=journal,title=title,author=author)
    except KeyError:
        p = Paper(journal=journal,
                  title=title,
                  author=a)
        p.put()
        return p.key()

def _addPlace(name, location, semester, year, placetype):
    """
    """
    assert issubclass(placetype,Place)
    try:
        return checkMembership(placetype,name=name, location=location)
    except KeyError:
        #might be cool to translate address into latlong
        p = placetype(name=name,
                      location=location,
                      semester=semester,
                      year=year)
        p.put()
        return p.key()

def addPlaceLive(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceLive)

def addPlaceEat(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceEat)

def addPlaceFun(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceFun)

def addPlaceStudy(name, location, semester, year):
    """
    """
    return _addPlace(name,location,semester,year, PlaceStudy)

def addInternship(company, location, semester, year):
    """
    """
    return _addPlace(company,location,semester,year,Internship)

def addGame(platform, title):
    """
    """
    try:
        return checkMembership(Game,title=title, platform=platform)
    except:
        g = Game(platform=platform,
                 title=title)
        g.put()
        return g.key()

def _addComment(text):
    c = Comment(text=text)
    c.put()
    return c.key()

def addRating(ratable, student, rating, comment=None):
    """
    """
    try:
        r = checkMembership(Rating,ratable=ratable,student=student)
    except KeyError:
        c = _addComment(comment)
        r = Rating(rated=ratable,
                   rater=student,
                   rating=int(rating),
                   comment=c)
    r.put()
    return r.key()
    
def checkMembership(classname, **kwargs):
    query = classname.all()
    for k in kwargs:
        query.filter(k + " =", kwargs[k])
    assert query.count() <= 1
    if query.count() == 1: return query.get().key()
    raise KeyError
