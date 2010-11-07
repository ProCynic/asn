from dataStore import *
import random
from dataAccessors import DataAccessor

##x = User.all().filter('userType =','STUDENT').get()
####x = Ratable.all().get()
DA = DataAccessor()
##DA.delete(x)

print issubclass(User, User)

for x in DA.dependencies: print x
