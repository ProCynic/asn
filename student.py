from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
import dataStore as DS
from dataAccessors import DataAccessor, addRatedTypename
from views import prepareRatingsForTemplate, unify

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
        
        ratings = prepareRatingsForTemplate(ratings, user)
        self.generate('student.html', {
            'ratings': ratings,
            'isStudentPage': True,
            'surpressFooter': True
        })

class StudentNewRating(BaseRequestHandler) :
    @user
    def get(self, typename=''):
        self.generate('studentNew.html', {
            'typename': typename,
            'surpressFooter': True
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

    def getUserRating(self, u, o) :
        rating = DS.Rating.all()
        rating.filter('rated =', o)
        rating.filter('rater =', u)
        return rating.get()

    @user
    def get(self, key=0):
        session = getSessionByRequest(self)
        user = getSessionUser(session)

        ratable = db.get(db.Key(key))
        
        session.deletionTarget = self.getUserRating(user, ratable);
        session.put()


        typename = str(ratable.__class__.__name__)
        self.generate('studentEdit.html', {
            'typename': typename,
            'rating': ratable,
            'surpressFooter': True,
        })

    @user
    def post(self, key=0):
        DA = DataAccessor()
        
        rated = db.get(db.Key(key))

        session = getSessionByRequest(self)
        user = getSessionUser(session)
        rating = self.getUserRating(user, rated)


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

class StudentDeleteRating(BaseRequestHandler) :
    @user 
    def get(self) :
        session = getSessionByRequest(self)
        if session.deletionTarget :
            
            da = DataAccessor()
            da.delete(session.deletionTarget)

            ratable = unify(session.deletionTarget.rated)
            setSessionMessage(session, "You have deleted " + ratable.name + ".")
            session.deletionTarget = None
            session.put()

        else :
            setSessionMessage(session, "Invalid request.")

        self.redirect('/student/')



class StudentPasswordPage(BaseRequestHandler):
    @user
    def get(self):
        """
            Shows the student password page.
        """

        session = getSessionByRequest(self)
        self.generate('studentPassword.html', {
            'surpressFooter': True,
            'allowUnconditionalChange': session.generated,
            # variables
        })

    @user
    def post(self):

        session = getSessionByRequest(self)
        user = getSessionUser(session)
        
        new = self.request.get('new')
        new2 = self.request.get('new2')

        if not session.generated :
            old = self.request.get('old')
            if (old != user.password) :
                setSessionMessage(session, "Your password was invalid.")
                self.redirect('/student/password/')
                return
    
        #Now, we have validated and can change our password.
        #Either we were generated, and get a change for free
        #or we've validated our password above.
        if (new != new2) :
            setSessionMessage(session, "Your new passwords did not match. Please try again.")
        else :
            setSessionMessage(session, "You have successfully changd your password.")
               
            #Reset the password
            user.password = new;
            user.put()

            #Reset the session.
            session.generated = False
            session.put()
            
        self.redirect('/student/')

