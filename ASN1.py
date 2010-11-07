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
DA.addAdmin('admin','000000')


class Login(BaseRequestHandler):
    def get(self):
        """
        """
        message = getSessionMessage(getSessionByRequest(self)) 
        self.generate('login.html', {
            'msg': message,
            'title': 'Login'
        })

    def post(self):
        uid = self.request.get('id')
        pw = self.request.get('pw')

        if not uid or not pw:
            setSessionMessageByRequest(self, "Please provide a User ID and Password to login.")
            self.redirect('/login')
        else:
            DA = DataAccessor()
            u = DA.getUser(uid, pw)
            if u is None:
                setSessionMessageByRequest(self, "The User ID and Password Combination you have provided was incorrect.")
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
                    setSessionMessageByRequest(self, "Invalid user")
                    self.redirect('/login')

class Logout(BaseRequestHandler):
    def get(self):     
        self.response.headers.add_header(
            'Set-Cookie', 
            'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT; path=/' % '')

        self.redirect('/browse')

class CreateUser(BaseRequestHandler):
    def post(self):
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

        user = DS.User.get(user)

        message  = "Your account has been created. Please store the following information in a secure location.<br/>"
        message += "<span class='credential'>UserID: %s</span><br/>" % user.uid
        message += "<span class='credential'>Password: %s</span><br/>" % user.password
        message += "<a href='/student/password'>Change Password</a>"


        setSessionMessage(session, message)

        self.redirect('/student')

class Ratable(BaseRequestHandler):
    @user
    def get(self,key=0):
        """
        """
        ratable = db.get(db.Key(key))
        unified = prepareItem(ratable) 
        
        ratings = DA.getAllRatings().filter('rated =',ratable)
        
        self.generate('ratable.html', {
            'ratable' : unified,
            'ratings': ratings
        })

class Sweep(BaseRequestHandler) :
    def get(self) :
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

class ManageUsersPage(BaseRequestHandler) :
    @admin
    def get(self):
        """
        """
        self.generate('manageUsers.html', {
        })

def main():
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
    ('/student/save/?', StudentSaveRating),
    ('/student/addrating/(.*)', StudentAddRating),
    ('/student/new/(.*)', StudentNewRating),
    ('/student/update/(.*)', StudentEditRating),
    ('/student/password/?', StudentPasswordPage),
    ('/student/deleteaccount/?', StudentDeleteAccount),
    ('/student/delete/?', StudentDeleteRating),
    ('/admin/?', AdminPage),
    ('/admin/export/?', AdminExport),
    ('/admin/import/?', AdminImport),
    ('/admin/clear/?', AdminClear),
    ('/admin/manageUsers/?', ManageUsersPage)
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
