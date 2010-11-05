from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
from dataAccessors import DataAccessor

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
        # assign new values
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


