from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
from dataAccessors import DataAccessor, addTypename
import dataStore as DS


def getAverageRating(item) :
    query = DS.Rating.all()
    query.filter('rated =', item)

    items = 0
    total = 0
    for x in query : 
        total += x.rating
        items += 1

    if items == 0 :
        return 100

    return (total / items, items);


def getRatingClass(rating) :
    if rating > 70 :
        return 'good' 
    
    if 70 >= rating > 40 :
        return 'average'

    return 'bad'


class Browser(BaseRequestHandler) :

    def get(self) :
        """
            Create the browser home page.
        """
        DA = DataAccessor()

        query = addTypename(DS.Ratable.all())

        temp = []
        for x in query :
            x.typename = x.__class__.__name__
            x.rating, x.ratingCount = getAverageRating(x)
            x.ratingClass = getRatingClass(x.rating)
            temp.append(x)






         
        
        ratings = DA.getAllRatings()
        self.generate('browser.html', {
            'title' : "Home",
            'ratings' : temp
        })
