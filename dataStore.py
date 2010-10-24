"""
	Defines the data models for the ASN
"""

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

class Person(db.Model):
	"""
		A model for Persons.

		A person has a first, middle and last name.
		However, the middle name is not required.
	"""
    fname = db.StringProperty(required=True)
    lname = db.StringProperty(required=True)
    mname = db.StringProperty()

class Student(db.Model):
	"""
		A model for Students

		A student has a random student id (sid)
		and a password.
	"""
    sid = db.StringProperty(required=True)
    password = db.StringProperty(required=True)

class Ratable(polymodel.PolyModel):
    """
		Ratable is the base class for ratable objects, and has 
		no inherent data.
    """
    pass

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
    rated = db.ReferenceProperty(Ratable)
    rater = db.ReferenceProperty(Student)

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

class Grade(db.Model):
    """
		The model for a Grade

    	A grade must be associated with a course, a student, and a grad.e
	"""
    course = db.ReferenceProperty(Course)
    student = db.ReferenceProperty(Student)
    grade = db.StringProperty(required=True, validator=gradeValidator)

class Book(Ratable):
    """
		The model for books.

		A book must have an isbn, a title and author.
		The author must be a person.
    """
    isbn = db.StringProperty()
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(Person,required=True)

class Paper(Ratable):
    """
		The model for papers.

		Papers must have type of either JOURNAL or CONFERENCE
		It must also have a title, and an author.
    """
    paperType = db.StringProperty(required=True,choices=['JOURNAL','CONFERENCE'])
    title = db.StringProperty(required=True)
    author = db.ReferenceProperty(Person,required=True)

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
