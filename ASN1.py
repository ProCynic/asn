import dataStore as DS
from exporter import export
from importer import StudentImporter
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

class BaseRequestHandler(webapp.RequestHandler):
  def generate(self, template_name, template_values={}):
	"""
	Generate a page with some default parameters. 
	Other parameters are received from the template_values.
	"""
	values = {
	  'request': self.request,
	  'debug': self.request.get('deb'),
	  'application_name': 'Anonymous Social Network, Phase 1',
	}
	values.update(template_values)
	directory = os.path.dirname(__file__)
	path = os.path.join(directory, os.path.join('templates', template_name))
	self.response.out.write(template.render(path, values, debug=_DEBUG))

class HomePage(BaseRequestHandler):
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
			Give the XML file up for download. This is exported from whatever was inside 
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
	
	def addErrorMessage(self, msg) :
		"""
			A callback to show messages.
		"""
		self.msg += msg

	# login required
	def post(self):
		"""
			Does the import and shows errors, if any.
		"""
		self.msg = ""
		si = StudentImporter(DataAccessor(self.addErrorMessage))
		try:
		    newFile = self.request.get('newFile')
		    si.parse(newFile)
		except IOError:
		    self.msg = "ERROR: Please select a file to import."

		if not self.msg :
			self.msg = "Import succeeded."

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
