from xml.etree import ElementTree
import sys
import dataAccessors as DA
import datastore


def addText(node, name, text) :
	subnode = addNode(node, name)
	subnode.text = text
	return subnode

def addNode(node, name) :
	subnode = ElementTree.SubElement(node, name)
	return subnode

def addRating(node, r) :
	addText(node, "rating", str(r.rating))
	addText(node, "comment", r.comment.text)

def personStr(r) :
	if (r.mname) :
		return r.fname + " " + r.mname + " " + r.lname
	else :
		return r.fname + " " + r.lname

class Exporter :
	def export(self, students) :
		root = ElementTree.Element("students")
		for s in students : 
			student = addNode(root, "student")

			for r in datastore.Rating.all().filter('rater =', s) :
				obj = r.rated;
				if isinstance(obj, datastore.Course) :
					grade = datastore.Grade.all().filter('course =', obj).filter('student =', s).get()
					self.exportCourse(student, r, obj, grade)
				elif isinstance(obj, datastore.Book) :
					self.exportBook(student, r, obj)
				else :
					print("")

		ElementTree.dump(root)

	def exportBook(self, p, rating, book) :
		c = addNode(p, 'book')
		addText(c, 'isbn', book.isbn)
		addText(c, 'title', book.title)
		addText(c, 'author', personStr(book.author))
		addRating(c, rating)

	def exportCourse(self, p, rating, course, grade) :
		c = addNode(p, "class")
		addText(c, "unique", course.unique)
		addText(c, "course_num", course.courseNum)
		addText(c, "course_name", course.name)
		addText(c, "semester", course.semester + " " + course.year)
		addText(c, "instructor", personStr(course.instructor))
		addText(c, "grade", grade.grade)
		addRating(c, rating)



e = Exporter()
e.export(datastore.Student.all())
