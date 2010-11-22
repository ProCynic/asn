import dataStore
import random
from dataAccessors import DataAccessor
from importer import Importer


print ''
print 'Hello World'

importer = Importer(DataAccessor())

filename = '/home/gparker/classes/373/asn2/xml/01-02.xml'

print filename

importer.parse(filename)
