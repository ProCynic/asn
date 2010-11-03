import os


from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

_DEBUG = True
class BaseRequestHandler(webapp.RequestHandler) :
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
