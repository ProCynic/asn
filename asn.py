import dataStore as DS
from export import export

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

class BaseRequestHandler(webapp.RequestHandler):
  def generate(self, template_name, template_values={}):
    values = {
      'request': self.request,
      'debug': self.request.get('deb'),
      'application_name': 'Anonymous Social Network, Part 1',
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

class HomePage(BaseRequestHandler):
    def get(self):
        self.generate('browser.html', {
            # variables
        })

class StudentPage(BaseRequestHandler):
    # login required
    def get(self):
        # fn's
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
        # fn's
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
        
        self.generate('admin.html', {
            # variables
        })
    def post(self):
        # fn's
        self.redirect('/admin')

class AdminExportPage(BaseRequestHandler):
    # login required
    def get(self):
        self.response.headers['Content-Type'] = "application/xml"
        export()

class AdminResetPage(BaseRequestHandler):
    # login required
    def get(self):
        # fn's
        self.generate('admin.html', {
            # variables
        })
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
    ('/', HomePage),
    ('/student', StudentPage),
    ('/student/password', StudentPasswordPage),
    ('/admin', AdminPage),
    ('/admin/export', AdminExportPage),
    ('/admin/reset', AdminResetPage)
  ], debug=_DEBUG)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
