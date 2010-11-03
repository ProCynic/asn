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
        message = self.request.get('m')
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
                self.response.headers.add_header(
                                                'Set-Cookie', 
                                                'ukey=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' \
                                                  % str(u.key()))
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
        #del self.response.headers['Set-Cookie']        
        self.response.headers.add_header(
                                        'Set-Cookie', 
                                        'ukey=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' \
                                          % '')
        self.redirect('/browse')

class CreateUser(BaseRequestHandler):
    def post(self):
        DA = DataAccessor()
        uid = userIDGen()
        pw = passwordGen()
        skey = str(DA.addStudent(uid, pw))
        self.response.headers.add_header(
                                        'Set-Cookie', 
                                        'ukey=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' \
                                          % skey)
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
    ('/browse', Browser),
    ('/ratable/(.*)', Ratable),
    ('/datastore\.xml', DatastoreXML),
    ('/login', Login),
    ('/logout', Logout),
    ('/createUser', CreateUser),
    ('/student', StudentPage),
    ('/student/password', StudentPasswordPage),
    ('/admin', AdminPage),
    ('/admin/export', AdminExport),
    ('/admin/import', AdminImport),
    ('/admin/reset', AdminReset)
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
