""" """

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
		raise Usage("Duplicate entry: " + str(err))


	def _addPerson(self, name) :
		name = name.strip().split()
		mname = None
		if len(name) == 2: fname,lname = name
		elif len(name) == 3: fname,mname,lname = name
		else: raise ValueError

		p = Person(fname=fname,
			   mname=mname,
			   lname=lname)

		pkey = ['fname', 'mname', 'lname']

		try:
			self._pkeyCheck(pkey, p)
			p.put()
			return p.key()
		except DataStoreClash as data:
			return data.entity
	
	def addStudent(self, uid, password) :
		s = User(uid=uid,
			 password=password
                         userType='STUDENT')
		pkey = ['uid', 'password']
		try:
			self._pkeyCheck(pkey, s)
			s.put()
			return s.key()
		except DataStoreClash as data:
			return data.entity

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
		author = self._addPerson(author)
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

	def addInternship(self, name, location, semester, year) :
		return self._addPlace(name, location, semester, year, Internship)

	def addRating(self, ratable, student, rating, comment=None) :
		c = self.addComment(comment)
		rating = int(rating)
		r = Rating(rating=rating,
			   rated=ratable,
			   rater=student,
			   comment=c)
		pkey = ['rated', 'rater']
		try:
			self._pkeyCheck(pkey, r)
		except DataStoreClash as data:
			r = data.entity
		finally:
			r.rating = rating
			r.comment = c
			r.put()
			return r.key()
		
	def addComment(self, text, replyto=None):
		c = Comment(text=text,
                            replyto=replyto)
		c.put()
		return c.key()

	def _addRatable(self, objtype, pkey, **assocs):
		r = objtype(**assocs)
		try:
			self._pkeyCheck(pkey, r)
			r.put()
			return r.key()
		except DataStoreClash as data:
			if data.entity == r: return data.entity.key()
			self._errHandler(data.entity)

	def _pkeyCheck(self, pkey, obj):
		objType = obj.__class__
		query = objType.all()
		for x in pkey:
			assert x in objType.properties()
			query.filter(x + ' =', getattr(obj, x))
		assert query.count() <= 1
		if query.count() == 1: raise DataStoreClash(query.get())
