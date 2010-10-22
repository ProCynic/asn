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
	addText(node, "rating", r.rating)
	addText(node, "comment", r.comment.text)

class Exporter :
	def export(self, students) :
		root = ElementTree.Element("students")
		for s in students : 
			student = addNode(root, "student")

			for r in datastore.Rating.all().filter('rater =', s) :
				obj = r.rated;
				if isinstance(obj, datastore.Course) :
					grade = datastore.Grade.all()
					print(type(grade))
					for g in grade :
						print(g.grade)
					self.exportCourse(student, r, obj, grade)

		



	def exportCourse(self, p, rating, course, grade) :
		c = addNode(p, "class")
		addText(c, "unique", course.unique)
		addText(c, "course_num", course.courseNum)
		addText(c, "course_name", course.name)
		addText(c, "semester", course.semester + " " + course.year)
		addText(c, "instructor", course.instructor)
		addRating(c, rating)



e = Exporter()
e.export(datastore.Student.all())
