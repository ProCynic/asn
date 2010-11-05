
""" """

from dataStore import *
from ourExceptions import *


class DataAccessor :
    def __init__(self, func=None) :
        if func: self._errHandler = func

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
        c = self.addComment(comment)
        rating = int(rating)
        pkey = ['rated', 'rater']
        return self._addItem(Rating, pkey,
                             rating=rating,
                             rated=ratable,
                             rater=student,
                             comment=c,
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

    def _pkeyCheck(self, pkey, obj):
        objType = obj.__class__
        query = objType.all()
        for x in pkey:
            assert x in objType.properties()
            query.filter(x + ' =', getattr(obj, x))
        assert query.count() <= 1
        if query.count() == 1: raise DataStoreClash(query.get())
