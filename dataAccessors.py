
""" """

from dataStore import *
from ourExceptions import *


"""
    Utility functions for views.

"""

def getUndecoratedTypename(item) :
    return item.__class__.__name__

def addTypename(query) :
    temp = []
    for x in query :
        x.typename = getUndecoratedTypename(x) 
        temp.append(x)
    return temp

def addRatedTypename(query) :
    temp = []
    for x in query :
        x.rated.typename = x.rated.__class__.__name__
        temp.append(x)
    return temp


class DataAccessor :
    def __init__(self, func=None) :
        if func: self._errHandler = func
        self.dependencies = {User : Rating,
                             Ratable : Rating,
                             Rating : Comment,
                             User : Grade,
                             User : Session,
                             Course : Grade}

    def _errHandler(self, err) :
        raise Usage("Duplicate entry: " + str(err))


    def _addPerson(self, name) :
        name = name.strip().split()
        mname = None
        if len(name) == 2: fname,lname = name
        elif len(name) == 3: fname,mname,lname = name
        else: raise ValueError

        pkey = ['fname', 'mname', 'lname']
        return self._addItem(Person, pkey,
                             fname=fname,
                             mname=mname,
                             lname=lname)
            

    def addUser(self, uid, password, userType):
        pkey = ['uid']
        return self._addItem(User, pkey,
                                 uid=uid,
                                 password=password,
                                 userType=userType)
    
    def addStudent(self, uid, password) :
        return self.addUser(uid, password, 'STUDENT')

    def addAdmin(self, uid, password):
        return self.addUser(uid, password, 'ADMIN')

    def addPaper(self, ptype, title, author) :
        author = self._addPerson(author)
        pkey = ['paperType', 'title', 'author']
        return self._addItem(Paper, pkey,
                             paperType=ptype.upper(),
                             title=title,
                             author=author)

    def addGrade(self, course, student, grade ) :
        pkey = ['course', 'student']
        return self._addItem(Grade, pkey,
                             course=course,
                             student=student,
                             grade=grade,
                             overwrite=True)
    
    def addCourse(self, unique, num, name, semester, year, instructor) :
        i = self._addPerson(instructor)
        pkey = ['unique']
        return self._addItem(Course, pkey,
                                unique=unique,
                                courseNum=num,
                                name=name,
                                semester=semester,
                                instructor=i,
                                year=year)

    def addBook(self, title, isbn, author) :
        author = self._addPerson(author)
        isbn = isbn.strip().replace('-','')
        pkey = ['isbn']
        return self._addItem(Book, pkey,
                             title=title,
                             isbn=isbn,
                             author=author)

    def addGame(self, platform, title):
        pkey = ['platform', 'title']
        return self._addItem(Game, pkey,
                             platform=platform,
                             title=title)

    def _addPlace(self, name, location, semester, year, ptype) :
        assert issubclass(ptype, Place)
        pkey = ['name', 'location', 'semester', 'year']
        return self._addItem(ptype, pkey,
                             name=name,
                             location=location,
                             semester=semester,
                             year=year)

    def addPlaceLive(self, name, location, semester, year) :
        return self._addPlace(name, location, semester, year, PlaceLive)

    def addPlaceEat(self, name, location, semester, year) :
        return self._addPlace(name, location, semester, year, PlaceEat)
     
    def addPlaceFun(self, name, location, semester, year) :
        return self._addPlace(name, location, semester, year, PlaceFun)
    
    def addPlaceStudy(self, name, location, semester, year) :
        return self._addPlace(name, location, semester, year, PlaceStudy)

    def addInternship(self, name, location, semester, year) :
        return self._addPlace(name, location, semester, year, Internship)

    def addRating(self, ratable, student, rating, comment=None) :
        if comment: comment = self.addComment(comment)
        rating = int(rating)
        pkey = ['rated', 'rater']
        return self._addItem(Rating, pkey,
                             rating=rating,
                             rated=ratable,
                             rater=student,
                             comment=comment,
                             overwrite=True)
    
    def addComment(self, text, replyto=None):
        c = Comment(text=text,
                    replyto=replyto)
        c.put()
        return c.key()

    def _addItem(self, objtype, pkey, overwrite=False, **assocs):
        r = objtype(**assocs)
        try:
            self._pkeyCheck(pkey, r)
            r.put()
            return r.key()
        except DataStoreClash, data:
            if data.entity == r: return data.entity.key()
            if overwrite: return self._updateItem(data.entity, r)
            self._errHandler(data.entity)


    def _updateItem(self, old, new):
        """
        Update the old item, in the datastore, to reflect the new item.
        """
        assert type(old) is type(new)
        for x in type(old).properties():
            setattr(old, x, getattr(new, x))
        return old


    def update(self, obj, **kwargs):
        assert obj.is_saved()
        assert issubclass(type(obj), db.Model)
        for x in kwargs:
            assert x in type(obj).properties()
            if x in ['instructor','author']:
                p = self._addPerson(kwargs[x])
                setattr(obj, x, p)
            else:
                setattr(obj, x, kwargs[x])
        obj.put()
        return obj

    def getUser(self, uid, pw):
        pkey = ['uid', 'password']
        u = User(uid=uid, password=pw, userType='STUDENT') # userType is ignored.  This is a hack to let us use _pkeyCheck.
        try:
            self._pkeyCheck(pkey, u)
            return None
        except DataStoreClash, err:
            return err.entity
    
    def getAllRatings(self):
        return Rating.all()
    
    def getRatingsByUser(self, user):
        ratings = Rating.all()
        ratings.filter('rater =', user.key())
        return ratings

    def delete(self, obj):
        assert issubclass(type(obj),db.Model)
        for x in self.dependencies:
            if type(obj) is x or issubclass(type(obj), x):
                for item in self.dependencies[x].all():
                    for prop in item:
                        if prop[1] == obj: self.delete(item)
        obj.delete()

    def clear(self, students=False):
        for x in Ratable.all(): self.delete(x)
        if students:
            for x in User.all():
                if x.userType == 'STUDENT': self.delete(x)
    

    def _pkeyCheck(self, pkey, obj):
        objType = obj.__class__
        query = objType.all()
        for x in pkey:
            assert x in objType.properties()
            query.filter(x + ' =', getattr(obj, x))
        assert query.count() <= 1
        if query.count() == 1: raise DataStoreClash(query.get())
