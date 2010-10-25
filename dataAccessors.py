"""
"""

from dataStore import *

class Usage (Exception):
	def __init__(self,msg):
	    self.msg = msg

class DataStoreClash (Exception):
        def __init__(self, entity):
                self.entity = entity


class DataAccessor :
	def __init__(self, func=None) :
		if func: self._errHandler = func

	def _errHandler(self, err) :
		raise Usage(err)


        def _addPerson(self, name) :
		name = name.strip().split()
		mname = None
		if len(name) == 2: fname,lname = name
		elif len(name) == 3: fname,mname,lname = name
		else: raise ValueError

		p = Person(fname=fname,
                           mname=mname,
                           lname=lname)

		pkeyMap = {'fname' : fname, 'mname' : mname, 'lname' : lname}

		try:
                        p = self._pkeyCheck(pkeyMap, p)
                        return p
                except DataStoreClash as data:
                        return data.entity
	
	def addStudent(self, sid, password) :
		return self.conditionalApply("Student", Student, self.primary(sid = sid), password = password)

	def addPaper(self, ptype, title, author) :
		author = self._addPerson(author)
		pkey = ['paperType', 'title', 'author']
		return self._addRatable(Paper, pkey,
                                        paperType=ptype,
                                        title=title,
                                        author=author)

	def addGrade(self, course, student, grade ) :
                pkey = ['course', 'student']
		return self._addRatable(Grade, pkey,
                                        course=course,
                                        student=student,
                                        grade=grade)
	
	def addCourse(self, unique, num, name, semester, year, instructor) :
		i = self._addPerson(instructor)
		pkey = ['unique']
		return self._addRatable(Course, pkey,
                                        unique=unique,
                                        courseNum=num,
                                        name=name,
                                        semester=semester,
                                        instructor=i,
                                        year=year)

	def addBook(self, title, isbn, author) :
		p = self._addPerson(author)
		isbn = isbn.strip().replace('-','')
		pkey = ['isbn']
		return self._addRatable(Book, pkey,
                                        title=title,
                                        isbn=isbn,
                                        author=author)

	def addGame(self, platform, title):
                pkey = ['platform', 'title']
		return self._addRatable(Game, pkey,
                                        platform=platform,
                                        title=title)

        def _addPlace(self, name, location, semester, year, ptype) :
		assert issubclass(ptype, Place)
		pkey = ['name', 'location', 'semester', 'year']
		return self._addRatable(ptype, pkey,
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

        def addInternship(self, company, location, semester, year) :
		return self._addPlace(company, location, semester, year, Internship)

	def addRating(self, ratable, student, rating, comment=None) :
		c = self.addComment(comment)
		r = Rating(rating=rating,
                           rated=ratable,
                           rater=student,
                           comment=c)
		pkeyMap= {'rated' : ratable, 'rater' : student}
		try:
                        r = self._pkeyCheck(pkeyMap, r)
                except DataStoreClash as data:
                        r = data.entity
                finally:
                        r.rating = rating
                        r.comment = c
                        r.put()
                        return r.key()
		
	def addComment(self, text):
                c = Comment(text=text)
                c.put()
                return c.key()

	def _addRatable(self, objtype, pkey, **assocs):
                r = objtype(assocs)
                pkeyMap = dict([x for x in assocs.items() if x[0] in pkey])
                try:
                        r = self._pkeyCheck(pkeyMap, r)
                        r.put()
                        return r.key()
                except DataStoreClash as data:
                        self._errHandler(data.entity)

        def _pkeyCheck(self, pkeymap, obj):
                objType = obj.kind()
                query = objType.all()
                for x in pkey:
                        assert x in objType.properties()
                        query.filter(x + ' =', getattr(obj, x))
                assert query.count() <= 1
                if query.count == 1: 
                        old = query.get()
                        for x in objType.properties():
                                if getattr(old, x) != getattr*=(obj, x):
                                        raise DataStoreClash(old)
                        return old
                return obj
