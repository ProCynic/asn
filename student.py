from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
from dataAccessors import DataAccessor, addRatedTypename
from views import prepareRatingsForTemplate

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
        
        ratings = prepareRatingsForTemplate(ratings)
        self.generate('student.html', {
            'ratings': ratings,
            'isStudentPage': True,

        })

class StudentNewRating(BaseRequestHandler) :
    @user
    def get(self, typename=''):
        self.generate('studentNew.html', {
            'typename': typename
        })

class StudentSaveRating(BaseRequestHandler) :
    @user
    def post(self):
        
        DA = DataAccessor()
        session = getSessionByRequest(self)
        user = getSessionUser(session)
        typename = self.request.get("typename")
        ratable = None
        
        if typename == 'Book':
            isbn = self.request.get('isbn')
            title = self.request.get('title')
            author = self.request.get('author')
            ratable = DA.addBook( title, isbn, author )
            
        elif typename == 'Paper':
            paperType = self.request.get('paperType').upper()
            title = self.request.get('title')
            author = self.request.get('author')
            ratable = DA.addPaper( paperType, title, author )
            
        elif typename == 'Course':
            unique = self.request.get('unique')
            courseNum = self.request.get('courseNum')
            name = self.request.get('name')
            semester = self.request.get('semester').upper()
            year = self.request.get('year')
            instructor = self.request.get('instructor')
            ratable = DA.addCourse( unique, courseNum, name, semester, year, instructor )
            
        elif typename == 'Game':
            platform = self.request.get('platform')
            title = self.request.get('title')
            ratable = DA.addGame( platform, title )
            
        elif typename in ['Internship', 'PlaceLive', 'PlaceEat', 'PlaceFun', 'PlaceLive', 'PlaceStudy'] :
            name = self.request.get('platform')
            location = self.request.get('title')
            semester = self.request.get('title')
            year = self.request.get('title')
            ratable = DA.addPlace( name, location, semester, year, typename )
        else :
            setSessionMessage(session, "Invalid rating type.")
            self.redirect('/student')
            
        if ratable :
            rating = self.request.get('rating')
            comment = self.request.get('comment')
            DA.addRating(ratable, user, rating, comment=comment)
        
        setSessionMessage(session, 'Successfully added new rating!')
        self.redirect('/student')

class StudentEditRating(BaseRequestHandler) :
    @user
    def get(self, key=0):
        rating = db.get(db.Key(key))
        typename = str(rating.__class__.__name__)
        self.generate('studentEdit.html', {
            'typename': typename,
            'rating': rating
        })


class StudentUpdateRating(BaseRequestHandler) :
    @user
    def post(self, key=0):
        DA = DataAccessor()
        rating = db.get(db.Key(key))
        rated = rating.rated
        typename = rated.__class__.__name__
        
        if typename == 'Book':
            isbn = self.request.get('isbn')
            title = self.request.get('title')
            #author = self.request.get('author')
            DA.update( rated, isbn=isbn, title=title )#, author=author )
        elif typename == 'Paper':
            paperType = self.request.get('paperType').upper()
            title = self.request.get('title')
            #author = self.request.get('author')
            DA.update( rated, paperType=paperType, title=title )#, author=author )
        elif typename == 'Course':
            unique = self.request.get('unique')
            courseNum = self.request.get('courseNum')
            name = self.request.get('name')
            semester = self.request.get('semester').upper()
            instructor = self.request.get('instructor')
            year = self.request.get('year')
            DA.update( rated, unique=unique, courseNum=courseNum, name=name, semester=semester, year=year ) # instructor=instructor
        elif typename == 'Game':
            platform = self.request.get('platform').upper()
            title = self.request.get('title')
            DA.update( rated, platform=platform, title=title )
        elif typename in ['Internship', 'PlaceLive', 'PlaceEat', 'PlaceFun', 'PlaceLive', 'PlaceStudy'] :
            name = self.request.get('platform')
            location = self.request.get('title')
            semester = self.request.get('semester').upper()
            year = self.request.get('year')
            DA.update( rated, name=name, location=location, semester=semester, year=year )
        
        DA.update(rating, rating=int(self.request.get('rating')))
        
        session = getSessionByRequest(self)
        setSessionMessage(session, 'Successfully updated rating!')
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


