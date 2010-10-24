import dataStore as DS
from exporter import export
from importer import StudentImporter
from dataAccessors import Usage
from importds import DataAccessor

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

class DatastoreXML(BaseRequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/xml"
        self.response.out.write(export())

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
        m = self.request.get('m')
        self.generate('admin.html', {
            'msg': m
        })
    def post(self):
        # fn's
        self.redirect('/admin')

class AdminExport(BaseRequestHandler):
    # login required
    def post(self):
        self.response.headers['Content-Type'] = "application/force-download"
        self.response.headers['Content-Disposition'] = "attachment; filename=\"datastore.xml\""
        self.response.headers['Content-Description'] = "File Transfer"
        self.response.out.write(export())

class AdminImport(BaseRequestHandler):
    # login required
    def post(self):
        si = StudentImporter(DataAccessor())
        try:
            newFile = self.request.get('newFile')
            si.parse(newFile)
            msg = "Import was successful."
        except IOError:
            msg = "ERROR: Please select a file to import."
        except Usage, err:
            msg = "ERROR: "+err.msg
        self.redirect('/admin?m='+msg)

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
    ('/', HomePage),
    ('/datastore\.xml', DatastoreXML),
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
