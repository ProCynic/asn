from dataStore import *
import dataAccessors

da = dataAccessors.DataAccessor()

c = da.addBook("The Ship Who Sang", '9780345334312' ,"Anne McCaffrey")

print ''
print c
print type(c)
