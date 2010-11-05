from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from views import *

from importer import Importer 
from dataAccessors import DataAccessor, addTypename
import dataStore as DS




class Browser(BaseRequestHandler) :

    def get(self) :
        """
            Create the browser home page.
        """
        DA = DataAccessor()

        query = prepareDataForTemplate(DS.Ratable.all())
        
        ratings = DA.getAllRatings()
        self.generate('browser.html', {
            'title' : "Home",
            'ratings' : query 
        })
