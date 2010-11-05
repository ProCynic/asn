from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
from dataAccessors import DataAccessor, addRatedTypename

class StudentPage(BaseRequestHandler) :
    @user
    def get(self):
        """
            Shows the student.html file, which 
            is supposed to be blank.
        """
        DA = DataAccessor()
        session = getSessionByRequest(self)
        user = getSessionUser(session)
        ratings = DA.getRatingsByUser(user)
        ratings = addRatedTypename(ratings)
        self.generate('student.html', {
            'ratings': ratings
        })

class StudentNewRating(BaseRequestHandler) :
    @user
    def post(self):
        # rating = Rating()
        # assign attributes from form # self.request.get('name'), etc
        self.redirect('/student')

class StudentUpdateRating(BaseRequestHandler) :
    @user
    def post(self, key=0):
        rating = db.get(db.Key(key))
        rated = rating.rated
        typename = rated.__class__.__name__
        
        if typename == 'Book':
            rated.isbn = self.request.get('isbn')
            rated.title = self.request.get('title')
            rated.author = self.request.get('author')
        elif typename == 'Paper':
            rated.paperType = self.request.get('paperType')
            rated.title = self.request.get('title')
            rated.author = self.request.get('author')
        elif typename == 'Course':
            rated.unique = self.request.get('unique')
            rated.courseNum = self.request.get('courseNum')
            rated.name = self.request.get('name')
            rated.semester = self.request.get('semester')
            rated.instructor = self.request.get('instructor')
            rated.year = self.request.get('year')
        elif typename == 'Game':
            rated.platform = self.request.get('platform')
            rated.title = self.request.get('title')
        elif typename == 'Internship' or typename == 'PlaceLive' or typename == 'PlaceEat' or typename == 'PlaceFun' or typename == 'PlaceLive' or typename == 'PlaceStudy':
            rated.name = self.request.get('platform')
            rated.location = self.request.get('title')
            rated.semester = self.request.get('title')
            rated.year = self.request.get('title')
            
        rating.rated = rated
        rating.put()
        self.redirect('/student')

class StudentPasswordPage(BaseRequestHandler):
    @user
    def get(self):
        """
            Shows the student password page.
        """
        self.generate('student.html', {
            # variables
        })
    @user
    def post(self):
        # ex1 = self.request.get('ex1')
        # fn's
        self.redirect('/edit')


