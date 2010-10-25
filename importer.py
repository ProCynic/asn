from xml.etree import ElementTree
import sys;
from importds import DataAccessor
import dataStore

"""
	This class provides a student descriptor.
	
	Data Members: 
		ID is the student ID
		password is the student password.
"""
class StudentDescriptor :
	ID = ""
	password = ""
	classes = []
	books = []
	papers = []
	interns = []
	places = []
	games = []

"""
	The following descriptors act as simple data stores.
"""
class PaperDescriptor : 
	pass 

class CourseDescriptor :
	pass

class BookDescriptor :
	pass

class InternDescriptor : 
	pass

class PlaceDescriptor : 
	pass

class GameDescriptor :
	pass

class StudentImporter :
	def __init__(self, data) :
		"""
			Create a student importer using the given import facade.
			The default DataAccessor will import into the datastore.
		"""
		self.DA = data
		self.parsingMap = {
			"StudentId" : (StudentDescriptor, "ID"),
			"StudentPassword" : (StudentDescriptor, "password"),

			"ClassUnique" : (CourseDescriptor, "unique"), 
			"ClassCourse_num" : (CourseDescriptor, "courseNum"),
			"ClassCourse_name" : (CourseDescriptor, "courseName"), 
			"ClassInstructor" : (CourseDescriptor, "instructor"),
			"ClassGrade" : (CourseDescriptor, "grade"),

			"BookIsbn" : (BookDescriptor, "isbn"),
			"BookTitle" : (BookDescriptor, "title"),
			"BookAuthor" : (BookDescriptor, "author"),

			"PaperPaper_category" : (PaperDescriptor, "category"), 
			"PaperTitle" : (PaperDescriptor, "title"),
			"PaperAuthor" : (PaperDescriptor, "author"),
		
			"InternPlace_name" : (InternDescriptor, "company"),
			"InternLocation" : (InternDescriptor, "location"),

			"PlacePlace_name" : (PlaceDescriptor, "place"),
			"PlaceLocation" : (PlaceDescriptor, "location"), 
		
			"GameOs" : (GameDescriptor, "OS"),
			"GameTitle" : (GameDescriptor, "title")
		}

	def __nullCallback(self, l) :
		return lambda x, y: sys.stdout.write("No such callback: " + l + "\n")

	def getFunctor(self, name, prefix, data) :
		"""
			Returns a function that handles the parsing of the input element, with the given prefix.
			Data is passed through to the function.
		"""
		invokeName = prefix.capitalize() + name.capitalize()

		#If the name is in the parsing map, return a simple set function over looking 
		if invokeName in self.parsingMap : 
			parsingValue = self.parsingMap[invokeName]
			if isinstance(data, parsingValue[0]) :
				return lambda element, data : setattr(data, parsingValue[1], element.text.strip())

		#Special case parsers.
		if (name.capitalize() == "Semester") : 
			return self.parseSemester

		if (name.capitalize() == "Rating") :
			return self.parseRating

		if (name.capitalize() == "Comment") : 
			return self.parseComment

		#Otherwise, try to look up the attribute.
		name = "parse" + invokeName
		callback = self.__nullCallback(name)
		try :
			callback = getattr(self, name)
		except AttributeError :
			#If no such attribute was found, return the default one.
			pass

		return callback

	def invokeChildren(self, p, prefix, data) :
		"""
			Recurse down the children of the element, invoking the parser at each element.
		"""
		for e in p :
			callback = self.getFunctor(e.tag, prefix, data)
			callback(e, data)

	def parse(self, xmlname) :
		"""
			Parse the given xml file.
		"""
		f = ElementTree.parse(xmlname)
		self.invokeChildren(f.getroot(), "", self)

	def parseStudent(self, e, d) :
		"""
			The parser for students. This will also add the student to the datastore
			through the stored DataAccessor, along with any other information provided.
		"""
		currentStudent = StudentDescriptor()
		self.invokeChildren(e, 'Student', currentStudent)
		
		DA = self.DA
		student = DA.addStudent(currentStudent.ID, currentStudent.password)

		#Add classes
		for c in currentStudent.classes :
			course = DA.addCourse(c.unique, c.courseNum, c.courseName, c.semester, c.year, c.instructor)
			DA.addGrade(course, student, c.grade)
			DA.addRating(course, student, c.rating, c.comment)

		#Add books
		for b in currentStudent.books :
			book = DA.addBook(b.title, b.isbn, b.author);
			DA.addRating(book, student, b.rating, b.comment)

		#Add papers
		for p in currentStudent.papers : 
			paper = DA.addPaper(p.category, p.title, p.author)
			DA.addRating(paper, student, p.rating, p.comment)

		#Add internships
		for i in currentStudent.interns : 
			internship = DA.addInternship(i.company, i.location, i.semester, i.year)
			DA.addRating(internship, student, i.rating, i.comment)

		#Add games
		for g in currentStudent.games :
			game = DA.addGame(g.OS, g.title)
			DA.addRating(game, student, g.rating, g.comment)

		#Add places
		for p in currentStudent.places :
			place = DA._addPlace(p.place, p.location, p.semester, p.year, p.typeID)
			DA.addRating(place, student, p.rating, p.comment)

	def parseStudentInternship(self, c, d) : 
		"""
			Parses an internship, and adds to the list. 
		"""
		newIntern = InternDescriptor();
		self.invokeChildren(c, "Intern", newIntern)
		d.interns.append(newIntern)

	def parseStudentStudy_place(self, c, d) : 
		"""
			Parses an study place, and adds to the list. 
		"""
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Study"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)

	def parseStudentLive_place(self, c, d) :
		"""
			Parses an study place, and adds to the list. 
		"""
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Live"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)

	def parseStudentEat_place(self, c, d) :
		"""
			Parses an eat place, and adds to the list. 
		"""
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Eat"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)

	def parseStudentFun_place(self, c, d) :
		"""
			Parses an fun place, and adds to the list. 
		"""
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Fun"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)
	
	def parseStudentClass(self, c, d) :
		"""
			Parses a class and adds to the list. 
		"""
		newClass = CourseDescriptor()
		self.invokeChildren(c, "Class", newClass)
		d.classes.append(newClass)

	def parseStudentBook(self, c, d) :
		"""
			Parses a book, and adds to the list. 
		"""
		newBook = BookDescriptor() 
		self.invokeChildren(c, "Book", newBook)
		d.books.append(newBook)

	def parseStudentPaper(self, c, d) : 
		"""
			Parses a paper, and adds to the list. 
		"""
		newPaper = PaperDescriptor()
		self.invokeChildren(c, "Paper", newPaper)
		d.papers.append(newPaper)

	def parseStudentGame(self, c, d) :
		"""
			Parses a game, and adds to the list. 
		"""
		newGame = GameDescriptor()
		self.invokeChildren(c, "Game", newGame)
		d.games.append(newGame)

	def parseSemester(self, c, d) : 
		"""
			Parses a semester, and adds to the list. 
		"""
		semester, year = c.text.strip().split()
		d.semester = semester.upper()
		d.year = year;

	def parseRating(self, c, d) :
		"""
			Parses out a rating.
		"""
		d.rating = c.text.strip()

	def parseComment(self, c, d) :
		"""
			Parses out a comment rating. 
		"""
		d.comment = c.text.strip()


