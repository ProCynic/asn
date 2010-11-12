import dataStore as DS
from exporter import export
from importer import Importer
from dataAccessors import DataAccessor
from ourExceptions import *

from acls import *
from baserequesthandler import BaseRequestHandler

from admin import *
from student import *
from browser import *
from session import *
from views import getRatingClass

import datetime
import os
import random
import re
import string
import sys
import wsgiref.handlers

from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import login_required


# Set to true if we want to have our webapp print stack traces, etc
_DEBUG = True

#default admin login
DA = DataAccessor()
try:
    DA.addAdmin('admin','000000')
except Usage:
    pass

class Login(BaseRequestHandler):
    def get(self):
        """
            Generates the login page.
        """
        self.generate('login.html', {
            'title': 'Login'
        })

    def post(self):
        """
            Attempts to log in a user.
            If the attempt fails, a message is shown.
            Otherwise, they are logged in and redirected to the 
            appropriate tools page.
        """
        uid = self.request.get('id')
        pw = self.request.get('pw')

        if not uid or not pw:
            setSessionMessageByRequest(self, "Please provide a User ID and Password to login.", True)
            self.redirect('/login')
        else:
            DA = DataAccessor()
            u = DA.getUser(uid, pw)
            if u is None:
                setSessionMessageByRequest(self, "The User ID and Password Combination you have provided was incorrect.", True)
                self.redirect('/login')
            else:
                sweepSessions()                
                session = generateSession(u.key())

                self.response.headers.add_header(
                    'Set-Cookie',
                    'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT; path=/' % str(session.sessionID))
                
                if u.userType == 'STUDENT':
                    self.redirect('/student')
                elif u.userType == 'ADMIN':
                    self.redirect('/admin')
                else :
                    setSessionMessageByRequest(self, "Invalid user", True)
                    self.redirect('/login')

class Logout(BaseRequestHandler):
    def get(self):     
        """
            Logs out the user by setting the cookie.
        """
        self.response.headers.add_header(
            'Set-Cookie', 
            'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT; path=/' % '')

        self.redirect('/browse')

class CreateUser(BaseRequestHandler):
    def post(self):
        """
            Creates a user, and will log him in.
            Will also show the user id, and prompt to change the password.
        """
        DA = DataAccessor()
        uid = userIDGen()
        pw = passwordGen()

        user = DA.addStudent(uid, pw)
        session = generateSession(user)
        session.generated = True;
        session.put()
       
        self.response.headers.add_header(
            'Set-Cookie', 
            'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT; path=/' % session.sessionID)

##        user = DS.User.get(user)

        message  = "Your account has been created. Please store the following information in a secure location.<br/>"
        message += "<span class='credential'>UserID: %s</span><br/>" % user.uid
        message += "<span class='credential'>Password: %s</span><br/>" % user.password
        message += "Change your password: <a href='/student/password'>Manage Account</a>"


        setSessionMessage(session, message, False)

        self.redirect('/student')

class Ratable(BaseRequestHandler):
    """
        Controller for showing the ratable page.
    """
    @user
    def get(self,key=0):
        """
            Shows the ratable page. This shows details about the ratable object, 
            along with all the ratings and their associated comments.
        """
        ratable = db.get(db.Key(key))
        user = getSessionUser(getSessionByRequest(self))
 
        temp = []
        ratings = DA.getAllRatings().filter('rated =',ratable)
        userRating = False

        for x in ratings :
            x.ratingclass = getRatingClass(x.rating) 
            if x.rater.key() == user.key() :
                userRating = True
            temp.append(x)
       
        unified = prepareItem(ratable, user)

        canEdit = len(temp) == 1 and userRating 

        self.generate('ratable.html', {
            'ratable' : unified,
            'ratings': temp,
            'user': user,
            'canEdit' : canEdit,
            'userRatingExists' : userRating,
        })

class Sweep(BaseRequestHandler) :
    def get(self) :
        """
            Sweeps the sessions. Any session over 20 minutes long
            will be invalidated.
        """
        sweepSessions()
        self.redirect('/')

class DatastoreXML(BaseRequestHandler):
    @admin
    def get(self):
        """
            Give the XML file up for download. This is exported from whatever was inuide 
            the datastore.
        """

        self.response.headers['Content-Type'] = "application/xml"
        self.response.out.write(export())



def main():
  """
    Setup the forwarding addresses.
  """
  application = webapp.WSGIApplication([
    ('/', Browser),
    ('/sweep/?', Sweep),
    ('/browse/?', Browser),
    ('/browse/([a-zA-Z]+)/?', Browser),
    ('/browse/([a-zA-Z]+)/([a-zA-Z]+)/?', Browser),
    ('/ratable/(.*)', Ratable),
    ('/datastore\.xml', DatastoreXML),
    ('/login/?', Login),
    ('/logout/?', Logout),
    ('/createUser/?', CreateUser),
    ('/student/?', StudentPage),
    ('/student/addrating/(.*)', StudentAddRating),
    ('/student/save/?', StudentSaveRating),
    ('/student/new/(.*)', StudentNewRating),
    ('/student/update/(.*)', StudentEditRating),
    ('/student/password/?', StudentPasswordPage),
    ('/student/deleteaccount/?', StudentDeleteAccount),
    ('/student/delete/?', StudentDeleteRating),
    ('/student/addgrade/?', StudentAddGrade),
    ('/admin/?', AdminPage),
    ('/admin/export/?', AdminExport),
    ('/admin/import/?', AdminImport),
    ('/admin/clear/?', AdminClear),
    ('/admin/manageUsers/?', ManageUsersPage),
    ('/admin/userdel/(.*)', UserDel),
    ('/admin/password/?', AdminPassword),
    ('/admin/newadmin/?', CreateAdmin),
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
