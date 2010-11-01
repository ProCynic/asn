from dataStore import *
import dataAccessors

da = dataAccessors.DataAccessor()

i = da._addPerson("Michelle Swenson")

print ''
pkey = ['fname', 'mname', 'lname']

c = Course(unique='55500',
           courseNum='M 358K',
           name='Stats',
           semester='FALL',
           year='2010',
           instructor=i)

d = Course(unique='55500',
           courseNum='M 358K',
           name='Stats',
           semester='FALL',
           year='2010',
           instructor=i)

print c.__class__
           
##query = Person.all()
##for x in pkey:
##    query.filter(x + ' =', getattr(p, x))
##print query.count()
##old = query.get()
##print old.fname, old.mname, old.lname
#da._pkeyCheck(pkey, p)
#da._addPerson('Geoffrey Parker')
#da._addPerson(b)
