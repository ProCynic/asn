from xml.etree import ElementTree
import sys;
import dataAccessors as DA
import dataStore


class StudentDescriptor :
	classes = []
	books = []
	papers = []
	interns = []
	places = []
	games = []

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

	def __init__(self) :
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
		print(self.parsingMap)

	def nullCallback(self, l) :
		return lambda x, y: sys.stdout.write("No such callback: " + l + "\n")

	def getFunctor(self, name, prefix, data) :
		
		invokeName = prefix.capitalize() + name.capitalize()

		if invokeName in self.parsingMap : 
			parsingValue = self.parsingMap[invokeName]
			if isinstance(data, parsingValue[0]) :
				return lambda element, data : setattr(data, parsingValue[1], element.text.strip())

		if (name.capitalize() == "Semester") : 
			return self.parseSemester

		if (name.capitalize() == "Rating") :
			return self.parseRating

		if (name.capitalize() == "Comment") : 
			return self.parseComment

		name = "parse" + invokeName
		callback = self.nullCallback(name)
		try :
			callback = getattr(self, name)
		except AttributeError :
			pass

		return callback

	def invokeChildren(self, p, prefix, data) :
		for e in p :
			callback = self.getFunctor(e.tag, prefix, data)
			callback(e, data)

	def parse(self, xmlname) :
		f = ElementTree.parse(xmlname)
		self.invokeChildren(f.getroot(), "", self)

	def parseStudent(self, e, d) :
		currentStudent = StudentDescriptor()
		self.invokeChildren(e, 'Student', currentStudent)
		
		student = DA.addStudent(currentStudent.ID, currentStudent.password)

		for c in currentStudent.classes :
			course = DA.addCourse(c.unique, c.courseNum, c.courseName, c.semester, c.year, c.instructor)
			DA.addGrade(course, student, c.grade)
			DA.addRating(course, student, c.rating, c.comment)

		for b in currentStudent.books :
			book = DA.addBook(b.title, b.isbn, b.author);
			DA.addRating(book, student, b.rating, b.comment)

		for p in currentStudent.papers : 
			paper = DA.addPaper(p.category, p.title, p.author)
			DA.addRating(paper, student, p.rating, p.comment)

		for i in currentStudent.interns : 
			internship = DA.addInternship(i.company, i.location, i.semester, i.year)
			DA.addRating(internship, student, i.rating, i.comment)

		for g in currentStudent.games :
			game = DA.addGame(g.OS, g.title)
			DA.addRating(game, student, g.rating, g.comment)

		for p in currentStudent.places :
			f = getattr(DA, "addPlace" + p.typeID)
			place = f(p.place, p.location, p.semester, p.year)
			DA.addRating(place, student, p.rating, p.comment)

	def parseStudentInternship(self, c, d) : 
		newIntern = InternDescriptor();
		self.invokeChildren(c, "Intern", newIntern)
		d.interns.append(newIntern)

	def parseStudentStudy_place(self, c, d) : 
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Study"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)

	def parseStudentLive_place(self, c, d) :
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Live"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)

	def parseStudentEat_place(self, c, d) :
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Eat"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)

	def parseStudentFun_place(self, c, d) :
		newPlace = PlaceDescriptor();
		newPlace.typeID = "Fun"
		self.invokeChildren(c, "Place", newPlace)
		d.places.append(newPlace)
	
	def parseStudentClass(self, c, d) :
		newClass = CourseDescriptor()
		self.invokeChildren(c, "Class", newClass)
		d.classes.append(newClass)

	def parseStudentBook(self, c, d) :
		newBook = BookDescriptor() 
		self.invokeChildren(c, "Book", newBook)
		d.books.append(newBook)

	def parseStudentPaper(self, c, d) : 
		newPaper = PaperDescriptor()
		self.invokeChildren(c, "Paper", newPaper)
		d.papers.append(newPaper)

	def parseStudentGame(self, c, d) :
		newGame = GameDescriptor()
		self.invokeChildren(c, "Game", newGame)
		d.games.append(newGame)

	def parseSemester(self, c, d) : 
		semester, year = c.text.strip().split()
		d.semester = semester.upper()
		d.year = year;

	def parseRating(self, c, d) :
		d.rating = c.text.strip()

	def parseComment(self, c, d) :
		d.comment = c.text.strip()

s = StudentImporter()
s.parse("test.xml")



































