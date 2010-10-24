"""
"""

import re
from dataStore import *

class Usage (Exception):
	def __init__(self,msg):
	    self.msg = msg

def _addPerson(name):
	"""
		Adds a person to the database, after splitting the 
		name into first, middle and last. 

		Does not add a person if they already exist in the data store.
		Returns the key of the person for further inserts concering this person.
	"""

	name = name.strip().split()
	mname = None
	if len(name) == 2: fname, lname = name
	elif len(name) == 3: fname, mname, lname = name
	else: raise ValueError

	try:
	    return checkMembership(Person,fname=fname, mname=mname, lname=lname)
	except KeyError:
	    p = Person(fname=fname,
	       lname=lname,
	       mname=mname)
	    p.put()
	    return p.key()

def addStudent(sid, password):
	"""
		Adds a student to the database.
		If they already exist, then we raise an error which will be displayed 
		on the user UI.

		Returns a key to the student for more inserts.
	"""
	try:
	    checkMembership(Student, sid=sid)
	    raise Usage("Duplicate Student IDs")
	except KeyError, e:
	    s = Student(sid=sid,
	                password=password)
	    s.put()
	    return s.key()

def addBook(title,isbn,author):
	"""
		Adds a book to the datastore. 
		If the book already exists, then we do not add anything.
		Otherwise, we add the person and book.

		Returns the key to the book for further inserts concerning this book.
	"""
	try:
	    return checkMembership(Book, isbn=isbn)
	except KeyError:
	    isbn = isbn.strip().replace('-','')
	    
	    a = _addPerson(author)
	    b = Book(title=title,
	             isbn=isbn,
	             author=a)
	    b.put()
	    return b.key()

def addCourse(unique, courseNum, name, semester, year, instructor):
	"""
		Adds a course to the database if it does not already exists.
		Returns the key to the course for more inserts concerning this course.
	"""
	try:
	    return checkMembership(Course, unique=unique)
	except KeyError:
	    i = _addPerson(instructor)
	    c = Course(unique=unique,
	    		courseNum=courseNum,
	    		name=name,
	    		semester=semester,
	    		year=year,
	    		instructor=i)
	c.put()
	return c.key()

def addGrade(course,student,grade):
	"""
		Adds a grade to the input course, for the input student, and the input grade.
		The course and students should be keys from previous inserts into the datastore.

		Returns a key to the grade in question.
	"""
	try:
	    return checkMembership(Grade, course=course, student=student)
	except KeyError:
		g = Grade(course=course,
	    		student=student,
	    		grade=grade)
		g.put()
		return g.key()

def addPaper(paperType, title, author):
	a = _addPerson(author)
	paperType = paperType.upper() #Make any insert conform to the xml schema inputs.
	try:
	    return checkMembership(Paper, paperType=paperType,title=title,author=author)
	except KeyError:
	    p = Paper(paperType=paperType,
	              title=title,
	              author=a)
	    p.put()
	    return p.key()

def _addPlace(name, location, semester, year, placetype):
	"""
	"""
	assert issubclass(placetype,Place)
	try:
	    return checkMembership(placetype,name=name, location=location)
	except KeyError:
	    #might be cool to translate address into latlong
	    p = placetype(name=name,
	                  location=location,
	                  semester=semester,
	                  year=year)
	    p.put()
	    return p.key()

def addPlaceLive(name, location, semester, year):
	"""
	"""
	return _addPlace(name,location,semester,year, PlaceLive)

def addPlaceEat(name, location, semester, year):
	"""
	"""
	return _addPlace(name,location,semester,year, PlaceEat)

def addPlaceFun(name, location, semester, year):
	"""
	"""
	return _addPlace(name,location,semester,year, PlaceFun)

def addPlaceStudy(name, location, semester, year):
	"""
	"""
	return _addPlace(name,location,semester,year, PlaceStudy)

def addInternship(company, location, semester, year):
	"""
	"""
	return _addPlace(company,location,semester,year,Internship)

def addGame(platform, title):
	"""
	"""
	try:
	    return checkMembership(Game,title=title, platform=platform)
	except:
	    g = Game(platform=platform,
	             title=title)
	    g.put()
	    return g.key()

def _addComment(text):
	c = Comment(text=text)
	c.put()
	return c.key()

def addRating(ratable, student, rating, comment=None):
	"""
	"""
	try:
	    r = checkMembership(Rating,ratable=ratable,student=student)
	except KeyError:
	    c = _addComment(comment)
	    r = Rating(rated=ratable,
	               rater=student,
	               rating=int(rating),
	               comment=c)
	r.put()
	return r.key()
	
def checkMembership(classname, **kwargs):
	query = classname.all()
	for k in kwargs:
	    query.filter(k + " =", kwargs[k])
	assert query.count() <= 1
	if query.count() == 1: return query.get().key()
	raise KeyError

class DataAccessor :
	def __init__(self, err = None) :
		if err :
			self.displayError = err
		else :
			self.displayError = self._displayError

	def _displayError(self, err) :
		raise Usage(err)


	def conditionalApply(self, cname, classID, primary, **secondary) :
		query = classID.all();
		for k in primary : 
			query.filter(k + " =", primary[k]);
	
		if query.count() == 1 :
			value = query.get()
			for k in secondary :
				if getattr(value, k) != secondary[k] :
					self.displayError("Attempted to add a duplicate " + cname)
					return query.get().key()
			return query.get().key()
	
		for k in secondary :
			primary[k] = secondary[k]
	
		f = classID(**primary)
		f.put()
		return f.key()

	def primary(self, **args) :
		return args

	def addPlace(self, ptype, name, location, semester, year) :
		getattr(self, "addPlace" + ptype)(name,location, semester, year)

	def addRating(self, ratable, student, rating, comment = None) :
		c = _addComment(comment)
		return self.conditionalApply("Rating", Rating, self.primary(rated = ratable, student = student), rating = int(rating), comment = c)
	
	def addStudent(self, sid, password) :
		return self.conditionalApply("Student", Student, self.primary(sid = sid), password = password)

	def addPaper(self, ptype, title, author) :
		p = self.addPerson(author)
		return self.conditionalApply("Paper", Paper, self.primary(paperType = ptype.upper(), title = title, author = p))

	def addPlaceLive(self, name, location, semester, year) :
		return self.conditionalApply("PlaceLive", PlaceLive, self.primary(name = name, location = location), semester = semester, year = year)

	def addPlaceEat(self, name, location, semester, year) :
		return self.conditionalApply("PlaceEat", PlaceEat, self.primary(name = name, location = location), semester = semester, year = year)
	 
	def addPlaceFun(self, name, location, semester, year) :
		return self.conditionalApply("PlaceFun", PlaceFun, self.primary(name = name, location = location), semester = semester, year = year)
	
	def addPlaceStudy(self, name, location, semester, year) :
		return self.conditionalApply("PlaceStudy", PlaceStudy, self.primary(name = name, location = location), semester = semester, year = year)
	
	def addPerson(self, name) :
		name = name.strip().split()
		mname = None
		if len(name) == 2: fname,lname = name
		elif len(name) == 3: fname,mname,lname = name

		return self.conditionalApply("Person", Person, self.primary(fname = fname, mname = mname, lname = lname))
	
	def addGrade(self, course, student, grade ) :
		return self.conditionalApply("Grade", Grade, self.primary(course = course, student = student), grade = grade)
	
	def addCourse(self, unique, num, name, semester, year, instructor) :
		p = self.addPerson(instructor)
		return self.conditionalApply("Course", Course, self.primary(unique = unique), courseNum = num, name = name, semester = semester, year = year, instructor = p)

	def addBook(self, title, isbn, author) :
		p = self.addPerson(author)
		return self.conditionalApply("Book", Book, self.primary(isbn=isbn), title = title, author = p)

	def addGame(self, platform, title) :
		return self.conditionalApply("Game", Game, self.primary(platform = platform, title = title))

	def addInternship(self, company, location, semester, year) :
		return self.conditionalApply("Internship", Internship, self.primary(name = company, location = location), semester = semester, year = year)

