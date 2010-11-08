from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from views import *

from importer import Importer 
from dataAccessors import DataAccessor, addTypename
import dataStore as DS

class Browser(BaseRequestHandler) :

    def get(self, arg = None, sort = None) :
        """
            Create the browser home page.
        """

        possiblemap = {
            "all" : DS.Ratable,
            "courses" : DS.Course, 
            "books" : DS.Book,
            "papers" : DS.Paper,
            "internships" : DS.Internship,
            "livingplaces" : DS.PlaceLive, 
            "eatingplaces" : DS.PlaceEat, 
            "funplaces" : DS.PlaceFun,
            "studyingplaces" : DS.PlaceStudy,
            "games" : DS.Game
        }

        if arg : 
            arg = arg.lower()

        if sort :
            sort = sort.lower()

        query = None
        if arg and arg in possiblemap :
            query = prepareDataForTemplate(possiblemap[arg].all())
        else :
            query = prepareDataForTemplate(DS.Ratable.all())

        if sort and sort in ['asc', 'desc'] :
            if sort == 'asc' :
                query = sorted(query, key= lambda x : x.rating)
            elif sort == 'desc' :
                query = sorted(query, key= lambda x : x.rating, reverse = True)

        if arg and not arg in possiblemap :
            setSessionMessage(getSessionByRequest(self), "That was an invalid query; showing all results instead.", True)

        
        self.generate('browser.html', {
            'title' : "Home",
            'ratings' : query,
            'arg' : arg,
            'sort' : sort
        })

    def post(self, unused = None, unused2 = None) :
        """
            Used to filter results when requested through the browser page.
        """
        filter = self.request.get('filter')
        if not filter :
            filter = 'all'

        sort = self.request.get('sort')

        if not sort :
            sort = 'desc'

        self.redirect('/browse/' + filter + "/" + sort)
