from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
import dataStore as DS
from dataAccessors import DataAccessor, addRatedTypename
from views import prepareRatingsForTemplate, unify, getUserRating, validRating, prepareItem
from google.appengine.ext.db import BadValueError

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
        """
            Shows the add rating page.
        """

        
        displaytypename = string.replace(typename, '-', ' ')
        typename = string.replace(typename, '-', '')


        self.generate('studentNew.html', {
            'display' : displaytypename,
            'typename': typename,
            'surpressFooter': True
        })

class StudentAddGrade(BaseRequestHandler) :
    @user
    def post(self) :
        """
            Handles adding grades to a course.
        """
        key = self.request.get('key')
        course = db.get(db.Key(key))
        
        session = getSessionByRequest(self)
        user = getSessionUser(session)
        
        da = DataAccessor()

        if (not self.request.get('grade')) :
            query = DS.Grade.all().filter('course =', course)
            query.filter('student =', user)
            
            grade = query.get()
            da.delete(grade)
            
            setSessionMessage(session, "Removed your grade", False)
            self.redirect('/ratable/%s' % key)
            return

        da.addGrade(course, getSessionUser(session), self.request.get('grade'))
        
        setSessionMessage(session, "Added your grade.", False)
        self.redirect('/ratable/%s' % key)

class StudentAddRating(BaseRequestHandler) :
    @user
    def get(self, key = None) :
        """
            Will display the add rating page.
        """
        session = getSessionByRequest(self)

        if not key :
            setSessionMessage(session, "Invalid Request.")
            self.redirect('/student/')
            return

        try :
            target = db.get(db.Key(key))
        except db.BadKeyError :
            setSessionMessageByRequest(self, "Invalid URL", True)
            self.redirect("/student/")
            return


        user = getSessionUser(session)

        rating = getUserRating(user, target)

        session.deletionTarget = rating;
        session.put()

        self.generate('studentAdd.html', {
            'surpressFooter': True,
            'ratable': prepareItem(target),
            'rating' : rating
        })

    @user
    def post(self, unused) :
        """
            Adds a rating to the given object.
        """
        session = getSessionByRequest(self)
    
        key = self.request.get('key')
        rating = self.request.get('rating')
        if (not validRating(rating)) :
            setSessionMessage(session, "Invalid rating.", False)
            self.redirect("/student/addrating/%s" % key)
            return

        target = db.get(db.Key(key))
        comment = self.request.get('comment')
        if not comment :
            comment = None

        da = DataAccessor()
        da.addRating(target, getSessionUser(session), rating, comment = comment)
        setSessionMessage(session, "Added Rating.", False)
        self.redirect("/student/")


class StudentSaveRating(BaseRequestHandler) :
    @user
    def post(self):
        """
            Saves a new rating into the datastore.
        """
        
        def errhandler(obj):
            raise DataStoreClash(obj)
        
        DA = DataAccessor(errhandler)
        session = getSessionByRequest(self)
        user = getSessionUser(session)
        typename = self.request.get("typename")
        ratable = None
        
        if typename == 'Book':
            isbn = self.request.get('isbn')
            title = self.request.get('title')
            author = self.request.get('author')
            try:
                ratable = DA.addBook( title, isbn, author )
            except BadValueError:
                setSessionMessage(session, "Enter all values.", True)
                self.redirect('/student/new/Book')
                return
            except ValueError:
                setSessionMessage(session, "Bad input syntax.", True)
                self.redirect('/student/new/Book')
                return
            except DataStoreClash, err:
                setSessionMessage(session, "Book already exists.", True)
                self.redirect('/ratable/'+str(err.entity.key()))
                return
            
        elif typename == 'Paper':
            paperType = self.request.get('paperType').upper()
            title = self.request.get('title')
            author = self.request.get('author')
            try:
                ratable = DA.addPaper( paperType, title, author )
            except BadValueError:
                setSessionMessage(session, "Enter all values.", True)
                self.redirect('/student/new/Paper')
                return
            except ValueError:
                setSessionMessage(session, "Bad input syntax.", True)
                self.redirect('/student/new/Paper')
                return
            except DataStoreClash, err:
                setSessionMessage(session, "Paper already exists.", True)
                self.redirect('/ratable/'+str(err.entity.key()))
                return
            
        elif typename == 'Course':
            unique = self.request.get('unique')
            courseNum = self.request.get('courseNum')
            name = self.request.get('name')
            semester = self.request.get('semester').upper()
            year = self.request.get('year')
            instructor = self.request.get('instructor')
            try:
                ratable = DA.addCourse( unique, courseNum, name, semester, year, instructor )
            except BadValueError:
                setSessionMessage(session, "Enter all values.", True)
                self.redirect('/student/new/Course')
                return
            except ValueError:
                setSessionMessage(session, "Bad input syntax.", True)
                self.redirect('/student/new/Course')
                return
            except DataStoreClash, err:
                setSessionMessage(session, "Course already exists.", True)
                self.redirect('/ratable/'+str(err.entity.key()))
                return
            
        elif typename == 'Game':
            platform = self.request.get('platform')
            title = self.request.get('title')
            try:
                ratable = DA.addGame( platform, title )
            except BadValueError:
                setSessionMessage(session, "Enter all values.", True)
                self.redirect('/student/new/Game')
                return
            except ValueError:
                setSessionMessage(session, "Bad input syntax.", True)
                self.redirect('/student/new/Game')
                return
            except DataStoreClash, err:
                setSessionMessage(session, "Game already exists.", True)
                self.redirect('/ratable/'+str(err.entity.key()))
                return
            
        elif typename in ['Internship', 'PlaceLive', 'PlaceEat', 'PlaceFun', 'PlaceLive', 'PlaceStudy'] :
            name = self.request.get('name')
            location = self.request.get('location')
            semester = self.request.get('semester')
            year = self.request.get('year')
            try:
                ratable = DA._addPlace(name, location, semester, year, getattr(DS, typename) )
            except BadValueError:
                setSessionMessage(session, "Enter all values.", True)
                self.redirect('/student/new/'+typename)
                return
            except ValueError:
                setSessionMessage(session, "Bad input syntax.", True)
                self.redirect('/student/new/'+typename)
                return
            except DataStoreClash, err:
                setSessionMessage(session, typename+" already exists.", True)
                self.redirect('/ratable/'+str(err.entity.key()))
                return
        else :
            setSessionMessage(session, "Invalid rating type.", True)
            self.redirect('/student')
            return
            
        if ratable :
            rating = self.request.get('rating')
            if (not validRating(rating)) :
                setSessionMessage(session, "Invalid rating, defaulting to 50", True)
                rating = '50'
            
            comment = self.request.get('comment')
            if not comment :
                comment = None
            DA.addRating(ratable, user, rating, comment=comment)
        
        self.redirect('/student')

class StudentEditRating(BaseRequestHandler) :

    @user
    def get(self, key=0):
        """
            Displays the edit rating page.
        """
        session = getSessionByRequest(self)
        user = getSessionUser(session)

        try :
            ratable = db.get(db.Key(key))
        except db.BadKeyError :
            setSessionMessageByRequest(self, "Invalid URL", True)
            self.redirect("/student/")
            return
        
        session.deletionTarget = getUserRating(user, ratable);
        session.put()

        rating = getUserRating(user, ratable)

        typename = str(ratable.__class__.__name__)
        self.generate('studentEdit.html', {
            'typename': typename,
            'rating': ratable,
            'surpressFooter': True,
            'score': rating
        })

    @user
    def post(self, key=0):
        """
            Edits the given rating.
        """
        DA = DataAccessor()
        
        rated = db.get(db.Key(key))

        session = getSessionByRequest(self)
        user = getSessionUser(session)
        rating = getUserRating(user, rated)


        if (not rating) :
            setSessionMessage(session, "You cannot edit something you have not rated.", True)
            self.redirect('/student')
            return

        q = DA.getAllRatings().filter("rated =", rated)
        if q.count() != 1 :
            setSessionMessage(session, "This item is no longer editable.", True);
            self.redirect("/student/")
            return

        typename = rated.__class__.__name__
        
        if typename == 'Book':
            isbn = self.request.get('isbn')
            title = self.request.get('title')
            author = self.request.get('author')
            DA.update( rated, isbn=isbn, title=title, author=author )
        elif typename == 'Paper':
            paperType = self.request.get('paperType').upper()
            title = self.request.get('title')
            author = self.request.get('author')
            DA.update( rated, paperType=paperType, title=title, author=author )
        elif typename == 'Course':
            unique = self.request.get('unique')
            courseNum = self.request.get('courseNum')
            name = self.request.get('name')
            semester = self.request.get('semester').upper()
            instructor = self.request.get('instructor')
            year = self.request.get('year')
            DA.update( rated, unique=unique, courseNum=courseNum, name=name, semester=semester, year=year, instructor=instructor )
        elif typename == 'Game':
            platform = self.request.get('platform').upper()
            title = self.request.get('title')
            DA.update( rated, platform=platform, title=title )
        elif typename in ['Internship', 'PlaceLive', 'PlaceEat', 'PlaceFun', 'PlaceLive', 'PlaceStudy'] :
            name = self.request.get('name')
            location = self.request.get('location')
            semester = self.request.get('semester').upper()
            year = self.request.get('year')
            DA.update( rated, name=name, location=location, semester=semester, year=year )
       
        if (validRating(self.request.get('rating'))) :
            DA.update(rating, rating=int(self.request.get('rating')))
            setSessionMessageByRequest(self, "Successfully updated rating.")
        else :
            setSessionMessageByRequest(self, "Invalid rating input. Keeping original", True)

       
        self.redirect('/student')

class StudentDeleteRating(BaseRequestHandler) :
    @user 
    def get(self) :
        """
            Deletes the object that has been stored in the session.
        """
        session = getSessionByRequest(self)

        if session.deletionTarget :
            da = DataAccessor()
            da.delete(session.deletionTarget)

            ratable = unify(session.deletionTarget.rated)
            setSessionMessage(session, "You have deleted " + ratable.name + ".")
            session.deletionTarget = None
            session.put()

        else :
            setSessionMessage(session, "Invalid request.", True)

        self.redirect('/student/')

class StudentDeleteAccount(BaseRequestHandler) :
    @user 
    def get(self) :
        """
            Deletes the current user.
        """
        session = getSessionByRequest(self) 
        user = getSessionUser(session)
        da = DataAccessor()
        da.delete(user)
        expireSession(session)
        self.redirect('/browse/') 

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
        """
            Changes the password of the current user.
            Will display error messages on failure through the session message system.
        """
        session = getSessionByRequest(self)
        user = getSessionUser(session)
        
        new = self.request.get('new')
        new2 = self.request.get('new2')
        
        if not new or not new2:
            setSessionMessage(session, "Enter password twice.", True)
            self.redirect('/student/password')
            return

        if not session.generated :
            old = self.request.get('old')
            if (old != user.password) :
                setSessionMessage(session, "Your password was invalid.", True)
                self.redirect('/student/password/')
                return
    
        #Now, we have validated and can change our password.
        #Either we were generated, and get a change for free
        #or we've validated our password above.
        if (new != new2) :
            setSessionMessage(session, "Your new passwords did not match. Please try again.", True)
        else :
            setSessionMessage(session, "You have successfully changed your password.", False)
               
            #Reset the password
            user.password = new;
            user.put()

            #Reset the session.
            session.generated = False
            session.put()
            
        self.redirect('/student/')

