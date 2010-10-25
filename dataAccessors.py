"""
"""

import re
from dataStore import *

class Usage (Exception):
	def __init__(self,msg):
	    self.msg = msg

def _addComment(text):
	c = Comment(text=text)
	c.put()
	return c.key()

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
			query = query.filter(k + " =", primary[k]);
	
		if query.count() == 1 :
			value = query.get()
			for k in secondary :
				if getattr(value, k) != secondary[k] :
					self.displayError("Attempted to add a duplicate " + cname + " " + k)
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
		return getattr(self, "addPlace" + ptype)(name,location, semester, year)

	def addRating(self, ratable, student, rating, comment = None) :
		if not comment :
			comment = "None"
	
		c = _addComment(comment)
		return self.conditionalApply("Rating", Rating, self.primary(rated = ratable, rater = student), rating = int(rating), comment = c)
	
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
		fname = ""
		lname= ""
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
		isbn = isbn.strip().replace('-','')
		return self.conditionalApply("Book", Book, self.primary(isbn=isbn), title = title, author = p)

	def addGame(self, platform, title) :
		return self.conditionalApply("Game", Game, self.primary(platform = platform, title = title))

	def addInternship(self, company, location, semester, year) :
		return self.conditionalApply("Internship", Internship, self.primary(name = company, location = location), semester = semester, year = year)

