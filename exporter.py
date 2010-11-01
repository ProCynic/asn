from xml.etree import ElementTree
from xml.dom import minidom
import sys
import dataAccessors as DA
import dataStore as DS


def addText(node, name, text) :
	"""
		Adds a text node to the input node element, with 
		the name and text given.
	"""
	subnode = addNode(node, name)
	subnode.text = text
	return subnode

def addNode(node, name) :
	"""
		Adds a node to the input node, with the given name.
	"""
	subnode = ElementTree.SubElement(node, name)
	return subnode

def addRating(node, r) :
	"""
		Adds a pair of rating text nodes to the input element.
	"""
	addText(node, "rating", str(r.rating))
	addText(node, "comment", r.comment.text)

def personStr(r) :
	"""
		Combines the first, middle and last name of the person 
		into a single person name.
	"""
	if (r.mname) :
		return r.fname + " " + r.mname + " " + r.lname
	else :
		return r.fname + " " + r.lname

nodetypes = {
	DS.PlaceLive : 'live_place',
	DS.PlaceEat : 'eat_place',
	DS.PlaceFun : 'fun_place',
	DS.PlaceStudy : 'study_place',
    DS.Internship : 'internship'
}

def export() :
	"""
		Exports all the s in the datastore out to an XML file.
	"""
        students = DS.User.all().filter('userType =','STUDENT')
        root = ElementTree.Element("students")
        for s in students : 
                student = addNode(root, "student")
                addText(student, "id", s.uid)
                addText(student, "password", s.password)
                for r in DS.Rating.all().filter('rater =', s) :
                        obj = r.rated;
                        if isinstance(obj, DS.Course) :
                            grade = DS.Grade.all().filter('course =', obj).filter('student =', s).get()
                            exportCourse(student, r, obj, grade)
                        elif isinstance(obj, DS.Book) :
                            exportBook(student, r, obj)
                        elif isinstance(obj, DS.Paper) :
                            exportPaper(student, r, obj)
                        elif isinstance(obj, DS.Game) :
                            exportGame(student, r, obj)
                        elif issubclass(type(obj), DS.Place) :
                            exportPlace(student, r, obj)
                        else: 
							assert False
                        
        xml = ElementTree.tostring(root)
        return minidom.parseString(xml).toprettyxml(indent="\t")
        

def exportCourse(p, rating, course, grade) :
	"""
		Exports a course instance to XML
	"""
        c = addNode(p, "class")
        addText(c, "unique", course.unique)
        addText(c, "course_num", course.courseNum)
        addText(c, "course_name", course.name)
        addText(c, "semester", course.semester.capitalize() + " " + course.year)
        addText(c, "instructor", personStr(course.instructor))
        addText(c, "grade", grade.grade)
        addRating(c, rating)

def exportBook(p, rating, book) :
	"""
		Exports a book instance into XML
	"""
        c = addNode(p, 'book')
        addText(c, 'isbn', book.isbn)
        addText(c, 'title', book.title)
        addText(c, 'author', personStr(book.author))
        addRating(c, rating)

def exportPaper(p, rating, paper):
	"""
		Exports a paper to XML
	"""
        c = addNode(p, 'paper')
        addText(c, 'paper_category', paper.paperType)
        addText(c, 'title', paper.title)
        addText(c, 'author', personStr(paper.author))
        addRating(c, rating)

def exportGame(p, rating, game):
	"""
		Exports a game to XML
	"""
        c = addNode(p, 'game')
        addText(c, 'title', game.title)
        addText(c, 'os', game.platform)
        addRating(c, rating)

def exportPlace(p, rating, place):
	"""
		Exports a place to XML. This encompases all places.
	"""
        c = addNode(p, nodetypes[type(place)])
        addText(c, 'place_name', place.name)
        addText(c, 'location', str(place.location))
        addText(c, "semester", place.semester.capitalize() + " " + place.year)
        addRating(c, rating)

