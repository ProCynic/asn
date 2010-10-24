import dataAccessors

class DataAccessor :
	def __init__(self) :
		pass

	def addStudent(self, studentID, password) :
		return dataAccessors.addStudent(studentID, password)

	def addCourse(self, unique, courseNumber, courseName, semester, year, instructor) :
		return dataAccessors.addCourse(unique, courseNumber, courseName, semester, year, instructor)
	
	def addGrade(self, course, student, grade) :
		return dataAccessors.addGrade(course, student, grade)

	def addRating(self, course, student, rating, comment) :
		return dataAccessors.addRating(course, student, rating, comment)

	def addBook(self, title, isbn, author) :
		return dataAccessors.addBook(title, isbn, author)

	def addPaper(self, category, title, author) :
		return dataAccessors.addPaper(category, title, author)

	def addInternship(self, company, location, semester, year) :
		return dataAccessors.addInternship(company, location, semester, year)

	def addGame(self, os, title) :
		return dataAccessors.addGame(os, title)

	def addPlace(self, tid, place, location, semester, year) :
		f = getattr(dataAccessors, 'addPlace' + tid)
		return f(place, location, semester, year)
