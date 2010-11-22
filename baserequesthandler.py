import os

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from session import *

_DEBUG = True
class BaseRequestHandler(webapp.RequestHandler) :
    def generate(self, template_name, template_values={}):
        """
        Generate a page with some default parameters. 
        Other parameters are received from the template_values.
        """

        session = getSessionByRequest(self)
        message, status = getSessionMessage(session)
        user = getSessionUser(session)

        values = {
          'request': self.request,
          'debug': self.request.get('deb'),
          'application_name': 'Anonymous Social Network',
          'user': user,
          'msg' : message,
          'msgstatus' : status
        }
        
        values.update(template_values)
        directory = os.path.dirname(__file__)
        path = os.path.join(directory, os.path.join('templates', template_name))
        self.response.out.write(template.render(path, values, debug=_DEBUG))
