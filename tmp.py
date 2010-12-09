from dataStore import *
import random
from dataAccessors import DataAccessor
from importer import Importer


from google.appengine.ext import db

##for x in Comment.all():
##    x.delete()
##
##for x in Rating.all():
##    x.delete()
##
##for x in Ratable.all():
##    x.delete()
##
##for x in Grade.all():
##    x.delete()


da = DataAccessor()

print ''
print 'Initial'
for x in Game.all():
    print x

g = da.addGame('ps3', "Assassin's Creed")

print 'After add'
for x in Game.all():
    print x

da.delete(g)

print 'After delete'
for x in Game.all():
    print x
