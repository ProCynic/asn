from dataStore import *
import random
from dataAccessors import DataAccessor

x = Ratable.all().get()

DA = DataAccessor()

DA.delete(x)
