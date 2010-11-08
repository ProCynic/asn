
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
    """
    A DataAccessor class.
    To modify the dataStore, create an object of this class and call the methods.
    """
    def __init__(self, func=None) :
        """
        The creator of the object can specify a custom error handler function.
        """
        if func: self._errHandler = func

        #used in delete for chain deletion
        self.dependencies = [(User, Rating),
                             (Ratable, Rating),
                             (Rating, Comment),
                             (User, Grade),
                             (User, Session),
                             (Course, Grade)]

    def _errHandler(self, err) :
        """
        The default error handler function.  Simply raises a usage exception.
        """
        raise Usage("Duplicate entry: " + str(err))


    def _addPerson(self, name) :
        """
        Add a person to the datastore.
        Takes a simple string.
        """
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
        """
        Add a user to the dataStore.
        """
        pkey = ['uid']
        return self._addItem(User, pkey,
                                 uid=uid,
                                 password=password,
                                 userType=userType)
    
    def addStudent(self, uid, password) :
        """
        Add a student to the dataStore.
        Uses addUser.
        """
        return self.addUser(uid, password, 'STUDENT')

    def addAdmin(self, uid, password):
        """
        Add an admin to the dataStore.
        Uses addUser.
        """
        return self.addUser(uid, password, 'ADMIN')

    def addPaper(self, ptype, title, author) :
        """
        Add a Paper to the dataStore.
        """
        author = self._addPerson(author)
        pkey = ['paperType', 'title', 'author']
        return self._addItem(Paper, pkey,
                             paperType=ptype.upper(),
                             title=title,
                             author=author)

    def addGrade(self, course, student, grade ) :
        """
        Add a grade to the dataStore.
        A grade is a relation between a student and a course.
        """
        pkey = ['course', 'student']
        return self._addItem(Grade, pkey,
                             course=course,
                             student=student,
                             grade=grade,
                             overwrite=True)
    
    def addCourse(self, unique, num, name, semester, year, instructor) :
        """
        Add a course to the datastore.
        Instructor is taken as a string.
        If a person by that name is already in the datastore, they become the instructor
        """
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
        """
        Add a book to the datastore.
        author is taken as a string.
        If a person by that name is already in the datastore, they become the instructor
        ISBN is taken as a string and must be a valid ISBN number
        """
        author = self._addPerson(author)
        isbn = isbn.strip().replace('-','')
        pkey = ['isbn']
        return self._addItem(Book, pkey,
                             title=title,
                             isbn=isbn,
                             author=author)

    def addGame(self, platform, title):
        """
        Add a game to the datastore
        """
        pkey = ['platform', 'title']
        return self._addItem(Game, pkey,
                             platform=platform,
                             title=title)

    def _addPlace(self, name, location, semester, year, ptype) :
        """
        Add a place to the datastore.
        This private method is called by the adders for all the subclasses of place.
        """
        assert issubclass(ptype, Place)
        pkey = ['name', 'location', 'semester', 'year']
        return self._addItem(ptype, pkey,
                             name=name,
                             location=location,
                             semester=semester,
                             year=year)

    def addPlaceLive(self, name, location, semester, year) :
        """
        Add a PlaceLive to the dataStore.
        Uses _addPlace
        """
        return self._addPlace(name, location, semester, year, PlaceLive)

    def addPlaceEat(self, name, location, semester, year) :
        """
        Add a PlaceEat to the dataStore.
        Uses _addPlace
        """
        return self._addPlace(name, location, semester, year, PlaceEat)
     
    def addPlaceFun(self, name, location, semester, year) :
        """
        Add a PlaceFun to the dataStore.
        Uses _addPlace
        """
        return self._addPlace(name, location, semester, year, PlaceFun)
    
    def addPlaceStudy(self, name, location, semester, year) :
        """
        Add a PlaceStudy to the dataStore.
        Uses _addPlace
        """
        return self._addPlace(name, location, semester, year, PlaceStudy)

    def addInternship(self, name, location, semester, year) :
        """
        Add an Internship to the dataStore.
        Uses _addPlace
        """
        return self._addPlace(name, location, semester, year, Internship)

    def addRating(self, ratable, student, rating, comment=None) :
        """
        Adds a rating to the datastore.
        A rating is a realtionship between a student and a ratable.
        Comments are optional.
        """
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
        """
        Adds a comment to the dataStore.
        """
        c = Comment(text=text,
                    replyto=replyto)
        c.put()
        return c.key()

    def _addItem(self, objtype, pkey, overwrite=False, **assocs):
        """
        Adds an item to the dataStore.
        All adders use this private method.
        If overwrite is True and there is already an object in the datastore with the same pkey, the old object will be overwritten.
        Otherwise the existing item is passed to the error handler fuction.
        """
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
        old.put()
        return old


    def update(self, obj, **kwargs):
        """
        Update the given object to have the specified properties"
        property names passed in kwargs must match property names of dataStore classes.
        """
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
        """
        Return the user with the specified uid and password.
        If not present, returns None.
        """
        pkey = ['uid', 'password']
        u = User(uid=uid, password=pw, userType='STUDENT') # userType is ignored.  This is a hack to let us use _pkeyCheck.
        try:
            self._pkeyCheck(pkey, u)
            return None
        except DataStoreClash, err:
            return err.entity
    
    def getAllRatings(self):
        """
        Return a query object containing all the ratings in the datastore.
        """
        return Rating.all()

    def getStudents(self):
        """
        Return a query object containing all the Students in the datastore.
        """
        return User.all().filter('userType =', 'STUDENT')

    def getAdmins(self):
        """
        Return a query object containing all the Admins in the datastore.
        """
        return User.all().filter('userType =', 'ADMIN')
    
    def getRatingsByUser(self, user):
        """
        Return a query object containing all the ratings made by the given user.
        """
        ratings = Rating.all()
        ratings.filter('rater =', user.key())
        return ratings

    def delete(self, obj):
        """
        Delete the given object.
        Chain deletes all the objects that reference this object in the dependencies table.
        """
        assert issubclass(type(obj),db.Model)
        for x, y in self.dependencies:
            if issubclass(type(obj), x):
                for item in y.all():
                    for prop in item:
                        if prop[1] == obj: self.delete(item)
        obj.delete()

    def clear(self, students=False):
        """
        Clear all Ratables, Ratings, and Grades from the datastore.
        """
        for x in Ratable.all(): self.delete(x)
        if students:
            for x in User.all():
                if x.userType == 'STUDENT': self.delete(x)
    

    def _pkeyCheck(self, pkey, obj):
        """
        Checks to see if there are any objects in the dataStore with the same primary key as the given object.
        If there are, raise a DataStoreClash with the existing object.
        """
        objType = obj.__class__
        query = objType.all()
        for x in pkey:
            assert x in objType.properties()
            query.filter(x + ' =', getattr(obj, x))
        assert query.count() <= 1
        if query.count() == 1: raise DataStoreClash(query.get())
