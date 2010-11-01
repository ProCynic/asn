from dataStore import *
import dataAccessors

x = Ratable.all().get()

print x.key()
