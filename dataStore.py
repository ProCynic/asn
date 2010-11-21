""" Defines the data models for the ASN """

from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from validators import *

class Comment(db.Model):
    """
        A model for Comments.

        These are associated generally with ratings.
        A comment is made of text, comment chains will require references to itself.
    """
    text = db.TextProperty(required=True)
    replyto = db.SelfReferenceProperty()

    def __str__(self):
        return str(self.text)

    def __iter__(self):
        yield ('text', self.text)

class Person(db.Model):
    """
        A model for Persons.

        A person has a first, middle and last name.
        However, the middle name is not required.
    """
    fname = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    mname = db.StringProperty()

    def __str__(self):
        s  = ""
        s += self.fname
        if self.mname: 
            s += ' i' + self.mname
        s += ' ' + self.lname
        return s

    def __iter__(self):
        d = self.__class__.properties()
        for x in d: 
            yield (x,getattr(self,x))

    def __eq__(self, other):
        if not issubclass(type(other), Person): return False
        for x,y in zip(self, other):
            if x != y: 
                return False
        return True



class User(db.Model):
    """
    A User.  Can be a student or admin.
    """
    uid = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    userType = db.StringProperty(required=True, choices=['STUDENT','ADMIN'])

    def __str__(self):
        s = ""
        s += "uid: " + self.uid + '\n'
        s += "password: " + self.password + '\n'
        return s

    def __iter__(self):
        d = self.__class__.properties()
        for x in d: yield (x,getattr(self,x))
            
    def __eq__(self, other):
        if not issubclass(type(other), User): return False
        for x,y in zip(self, other):
            if x != y: return False
        return True
    
class Ratable(polymodel.PolyModel):
    """
        Ratable is the base class for ratable objects, and has 
        no inherent data.
    """

    def __str__(self):
        s = ""
        for p in self.__class__.properties():
              if p[0] != '_': s += p + ": " + str(getattr(self, p)) + '\n'
        return s

    def __iter__(self):
        d = self.__class__.properties()
        try:
            d.pop('_class')
        except KeyError:
            print ''
            print self.__class__.properties()
        for x in d: yield (x, getattr(self, x))

    def __eq__(self, other):
        if not issubclass(type(other), Ratable): return False
        for x,y in zip(self, other):
            if x != y: return False
        return True

class Rating(db.Model):
    """
        A model for Ratings.

        A rating has the rating itself, 
        a comment which may have a comment chain,
        the rated object
        and the rater that did the rating.
    """
    rating = db.RatingProperty(required=True)
    comment = db.ReferenceProperty(Comment)
    rated = db.ReferenceProperty(Ratable, required=True)
    rater = db.ReferenceProperty(User, required=True, validator=studentValidator)

    def __iter__(self):
        d = self.__class__.properties()
        for x in d: yield (x,getattr(self,x))

class Course (Ratable):
    """
        The model for Courses

        A course has unique number, course number, and name.
        It also has a semseter, instructor and year.

    """
    unique = db.StringProperty(required=True,validator=uniqueValidator)
    courseNum = db.StringProperty(required=True, validator=courseNumValidator)
    name = db.StringProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    instructor = db.ReferenceProperty(Person, required=True)
    year = db.StringProperty(required=True, validator=yearValidator)

    def __str__(self):
        s = """Unique: %s
        Course #: %s
        Name: %s
        """ % (self.unique, self.courseNum, self.name)
        return s.replace('\n','<br />')

class Grade(db.Model):
    """
        The model for a Grade

        A grade must be associated with a course, a student, and a grad.e
    """
    course = db.ReferenceProperty(Course, required=True)
    student = db.ReferenceProperty(User, required=True, validator=studentValidator)
    grade = db.StringProperty(required=True, validator=gradeValidator)

    def __str__(self):
                return str(self.grade)

    def __iter__(self):
        d = self.__class__.properties()
        for x in d: yield (x, getattr(self, x))

class Book(Ratable):
    """
        The model for books.

        A book must have an isbn, a title and author.
        The author must be a person.
    """
    isbn = db.StringProperty(validator=isbnValidator)
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(Person,required=True)

    def __str__(self):
        s = """Title: %s
        Author: %s
        ISBN: %s
        """ % (self.title, str(self.author), self.isbn)
        return s.replace('\n','<br />')

class Paper (Ratable):
    """
        The model for papers.

        Papers must have type of either JOURNAL or CONFERENCE
        It must also have a title, and an author.
    """
    paperType = db.StringProperty(required=True,choices=['JOURNAL','CONFERENCE'])
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(Person,required=True)

    def __str__(self):
        s = """Title: %s
        Author: %s
        Paper Type: %s
        """ % (self.title, str(self.author), self.paperType.capitalize())
        return s.replace('\n','<br />')

class Place (Ratable):
    """
        The model for a place.

        A place must have a name, location, semester, and year.
        Latitude and longitude is optional, but are a future feature.
    """
    name = db.StringProperty(required=True)
    location = db.PostalAddressProperty(required=True)
    semester = db.StringProperty(required=True,choices=['FALL','SPRING','SUMMER'])
    year = db.StringProperty(required=True,validator=yearValidator)
    #might be cool to do latlong
    latLong = db.GeoPtProperty()

class Internship (Place):
    """
        The model for an Internship

        No additional data is required over what is given for a Place.
    """
    pass

class PlaceLive (Place):
    """
        The model for a living area.

        No additional data is required over what is given for a Place.
    """
    pass

class PlaceEat (Place):
    """
        The model for a eating place.

        No additional data is required over what is given for a place.
    """
    pass

class PlaceFun (Place):
    """
        The model for a fun place.

        No additional data is required over what is given for a place.
    """
    pass

class PlaceStudy (Place):
    """
        The model for a study area.

        No additional data is required over what is given for a place.
    """
    pass

class Game (Ratable):
    """
        The model for a game.

        A game has a platform and a title.
    """
    platform = db.StringProperty(required=True)
    title = db.StringProperty(required=True)

class Session(db.Model) :
    """
    The model for a session.
    Used to keep track of who is logged in.
    """
    sessionID = db.StringProperty(required=True)
    user = db.ReferenceProperty(User)
    message = db.StringProperty()
    msgstatus = db.BooleanProperty(default=False)
    generated = db.BooleanProperty(required=True)
    expiration = db.DateTimeProperty(required=True)
    
    deletionTarget = db.ReferenceProperty(Rating)
    confirmedDelete = db.BooleanProperty(default=False)

    def __iter__(self):
        d = self.__class__.properties()
        for x in d: yield (x, getattr(self, x)) 

