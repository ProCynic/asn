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

x = DataAccessor()
x.addAdmin('admin','000000')
del x

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


def user(func):
    def redirectlogin(self):
        return self.redirect('/login?msg=Login%20Required')
    def checkauth(*args, **kwargs):
        ukey = args[0].request.cookies.get('ukey', '')
        u = db.get(db.Key(ukey))
        if u is None:
            return redirectlogin(args[0])
        if u.userType == 'STUDENT':
            return func(*args, **kwargs)
        return redirectlogin(args[0])
    return checkauth

def admin(func):
    def redirectlogin(self):
        return self.redirect('/login?msg=Login%20Required')
    def checkauth(*args, **kwargs):
        ukey = args[0].request.cookies.get('ukey', '')
        u = db.get(db.Key(ukey))
        if u is None:
            return redirectlogin(args[0])
        if u.userType == 'ADMIN':
            return func(*args, **kwargs)
        return redirectlogin(args[0])
    return checkauth



class BaseRequestHandler(webapp.RequestHandler):
  def generate(self, template_name, template_values={}):
    """
    Generate a page with some default parameters. 
    Other parameters are received from the template_values.
    """
    ukey = self.request.cookies.get('ukey', '')
    if ukey == '':
        user = None
    else:
        user = db.get(db.Key(ukey))
    values = {
      'request': self.request,
      'debug': self.request.get('deb'),
      'application_name': 'Anonymous Social Network, Phase 2',
      'user': user
    }
    values.update(template_values)
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, os.path.join('templates', template_name))
    self.response.out.write(template.render(path, values, debug=_DEBUG))

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
        self.generate('login.html', {
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
                self.redirect('/login')
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
        uid = uidgen()
        pw = passgen()
        skey = str(DA.addStudent(uid, pw))
        self.response.headers.add_header(
                                        'Set-Cookie', 
                                        'ukey=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT' \
                                          % skey)
        self.redirect('/student')

class Browser(BaseRequestHandler):
    def get(self):
        """
           Create the home page with some default parameters. 
        """
        self.generate('browser.html', {
            'title': 'Home'
        })

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

class StudentPage(BaseRequestHandler):
    @user
    def get(self):
        """
            Shows the student.html file, which 
            is supposed to be blank.
        """
        self.generate('student.html', {
            # variables
        })
    @user
    def post(self):
        # ex1 = self.request.get('ex1')
        # fn's
        self.redirect('/edit')

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

class AdminPage(BaseRequestHandler):
    @admin
    def get(self):
        m = self.request.get('m')
        self.generate('admin.html', {
            'msg': m,
            'title': 'Admin'
        })
    @admin
    def post(self):
        # fn's
        self.redirect('/admin')

class AdminExport(BaseRequestHandler):
    @admin
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

        @admin
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
    @admin
    def post(self):
        """
        a = comment.all()
        for b in a:
            b.delete()
        # etc for all classes, except person?
        """
        self.redirect('/admin')
        
class CreateAdmin(BaseRequestHandler):
    @admin
    def post(self):
        DA = DataAccessor()
        uid = uidgen()
        pw = passgen()
        DA.addAdmin(uid, pw)
        self.redirect('/admin')

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
