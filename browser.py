from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
from dataAccessors import DataAccessor

class Browser(BaseRequestHandler) :
    
    def get(self) :
        """
            Create the browser home page.
        """
        DA = DataAccessor()
        ratings = DA.getAllRatings()
        self.generate('browser.html', {
            'title' : "Home",
            'ratings' : ratings
        })
