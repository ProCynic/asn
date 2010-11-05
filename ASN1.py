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
x = DataAccessor()
x.addAdmin('admin','000000')
del x


class Login(BaseRequestHandler):
    def get(self):
        """
        u = loggedIn()
        if u is not None:
            if u.userType == 'STUDENT':
                self.redirect('/student')
                return
            elif u.userType == 'ADMIN':
                self.redirect('/admin')
                return
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
            self.redirect('/login')
            return
        else:
            DA = DataAccessor()
            u = DA.getUser(uid, pw)
            if u is None:
                self.redirect('/login?m=User%20ID%2FPassword%20combination%20incorrect.')
                return
            else:
                sweepSessions()                
                session = generateSession(u.key())

                self.response.headers.add_header(
                    'Set-Cookie',
                    'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' % str(session.sessionID))

                if u.userType == 'STUDENT':
                    self.redirect('/student')
                    return
                elif u.userType == 'ADMIN':
                    self.redirect('/admin')
                    return
        #assert "Somebody screwed the datastore" and False
        
        print u
        self.redirect('/login')

class Logout(BaseRequestHandler):
    def get(self):     
        self.response.headers.add_header(
                                        'Set-Cookie', 
                                        'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' \
                                          % '')
        self.redirect('/browse')

class CreateUser(BaseRequestHandler):
    def post(self):
        DA = DataAccessor()
        uid = userIDGen()
        pw = passwordGen()

        user = DA.addStudent(uid, pw)
        session = generateSession(user)
       
        self.response.headers.add_header(
                                        'Set-Cookie', 
                                        'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' \
                                          % session.sessionID)
        setSessionMessage(session, str(DS.User.get(user)).replace('\n','<br />'))
        self.redirect('/student')

class Ratable(BaseRequestHandler):
    def get(self,key=0):
        """
        """
        ratable = db.get(db.Key(key))
        if hasattr(ratable,'name'):
            title = ratable.name
        elif hasattr(ratable,'title'):
            title = ratable.title
        else:
            assert False
        ratableType = str(type(ratable))[18:-2]
        ratings = DS.Rating.all().filter('rated =',ratable)
        self.generate('ratable.html', {
            'title': title + ' ('+ratableType+')',
            'type' : ratableType,
            'content': str(ratable),
            'ratings': ratings
        })

class Sweep(BaseRequestHandler) :
    def get(self) :
        sweepSessions()
        self.redirect('/')

class Session(BaseRequestHandler) :
    def get(self) :
        sessions = DS.Session.all()
        for s in sessions : 
            if (s.user) :
                print(s.sessionID + " " + str(s.user))
            else :
                print(s.sessionID)
        print("!") 

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
  application = webapp.WSGIApplication([
    ('/', Browser),
    ('/session', Session),
    ('/sweep', Sweep),
    ('/browse', Browser),
    ('/ratable/(.*)', Ratable),
    ('/datastore\.xml', DatastoreXML),
    ('/login', Login),
    ('/logout', Logout),
    ('/createUser', CreateUser),
    ('/student', StudentPage),
    ('/student/new', StudentNewRating),
    ('/student/update/(.*)', StudentUpdateRating),
    ('/student/password', StudentPasswordPage),
    ('/admin', AdminPage),
    ('/admin/export', AdminExport),
    ('/admin/import', AdminImport),
    ('/admin/reset', AdminReset)
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
