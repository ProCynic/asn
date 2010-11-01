import dataStore as DS
from exporter import export
from importer import Importer
from dataAccessors import Usage, DataAccessor

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

def randString(n):
        alphanum = "abcdefghijklmnopqrstuvwxyz"
        alphanum += alphanum.upper()
        alphanum += "0123456789"
        alphanum += "~!@#$%^&*()-_=+:;/?"
        string = ""
        gen = random.Random()
        for x in range(n):
                string += alphanum[gen.randint(0,len(alphanum)-1)]
        return string
def uidgen():
        return randString(8)
def passgen():
        return randString(12)

class BaseRequestHandler(webapp.RequestHandler):
  def generate(self, template_name, template_values={}):
    """
    Generate a page with some default parameters. 
    Other parameters are received from the template_values.
    """
    values = {
      'request': self.request,
      'debug': self.request.get('deb'),
      'application_name': 'Anonymous Social Network, Phase 2',
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class Login(BaseRequestHandler):
    def get(self):
        self.generate('login.html', {
            'title': 'Login'
        })
    def post(self):
        uid = self.request.get('id')
        pw = self.request.get('pw')
        if not uid or not pw:
            self.redirect('/login')
        else:
            DA = DataAccessor()
            u = DA.getUser(uid, pw)
            if u is None:
                self.redirect('/login')
            elif u.userType == 'STUDENT':
                self.redirect('/student')
            elif u.userType == 'ADMIN':
                self.redirect('/admin')
        assert "Somebody screwed the datastore" and False
        self.redirect('/login')

class Browser(BaseRequestHandler):
    def get(self):
        """
           Create the home page with some default parameters. 
        """
        self.generate('browser.html', {
            'title': 'Home'
        })

class DatastoreXML(BaseRequestHandler):
    def get(self):
        """
            Give the XML file up for download. This is exported from whatever was inuide 
            the datastore.
        """

        self.response.headers['Content-Type'] = "application/xml"
        self.response.out.write(export())

class StudentPage(BaseRequestHandler):
    # login required
    def get(self):
        """
            Shows the student.html file, which 
            is supposed to be blank.
        """
        self.generate('student.html', {
            # variables
        })
    def post(self):
        # ex1 = self.request.get('ex1')
        # fn's
        self.redirect('/edit')

class StudentPasswordPage(BaseRequestHandler):
    # login required
    def get(self):
        """
            Shows the student password page.
        """
        self.generate('student.html', {
            # variables
        })
    def post(self):
        # ex1 = self.request.get('ex1')
        # fn's
        self.redirect('/edit')

class AdminPage(BaseRequestHandler):
    # login required
    def get(self):
        m = self.request.get('m')
        self.generate('admin.html', {
            'msg': m,
            'title': 'Admin'
        })
    def post(self):
        # fn's
        self.redirect('/admin')

class AdminExport(BaseRequestHandler):
    # login required
    def get(self):
        self.generate('export.html', {
            'xml': export(),
            'title': 'Admin'
        })

class AdminImport(BaseRequestHandler):

        
        def addErrorMessage(self, obj) :
                """
                A callback to show messages.
                """
                self.msg += "Duplicate " + str(obj.__class__).strip('<>') + ' ' + str(obj).replace('\n',"<br/>") + '<br/>'

        # login required
        def post(self):
                """
                Does the import and shows errors, if any.
                """
                self.msg = ""
                si = Importer(DataAccessor(self.addErrorMessage))
                #si = Importer()
                try:
                    newFile = self.request.get('newFile')
                    si.parse(newFile)
                except IOError:
                    self.msg = "ERROR: Please select a file to import."

                except Usage, err:
                    self.msg = err.msg

                if not self.msg :
                        self.msg = "Import succeeded."
        
                if len(self.msg) > 512 :
                        self.msg = self.msg[0:512] + "..."


                self.redirect('/admin?m='+self.msg)

class AdminReset(BaseRequestHandler):
    # login required
    def post(self):
        """
        a = comment.all()
        for b in a:
            b.delete()
        # etc for all classes, except person?
        """
        self.redirect('/admin')

def main():
  application = webapp.WSGIApplication([
    ('/', Browser),
    ('/browse', Browser),
    ('/datastore\.xml', DatastoreXML),
    ('/login', Login),
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
