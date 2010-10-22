from xml.etree import ElementTree
import sys
import dataAccessors as DA
import dataStore as DS


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

nodetypes = {
	DS.PlaceLive : 'live_place',
	DS.PlaceEat : 'eat_place',
	DS.PlaceFun : 'fun_place',
	DS.PlaceStudy : 'study_place',
        DS.Internship : 'internship'
	}




def export() :
        students = DS.Student.all()
        print nodetypes
        root = ElementTree.Element("students")
        for s in students : 
                student = addNode(root, "student")
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
                        else: assert False
                        

        print ''
        ElementTree.dump(root)
        

def exportCourse(p, rating, course, grade) :
        c = addNode(p, "class")
        addText(c, "unique", course.unique)
        addText(c, "course_num", course.courseNum)
        addText(c, "course_name", course.name)
        addText(c, "semester", course.semester + " " + course.year)
        addText(c, "instructor", personStr(course.instructor))
        addText(c, "grade", grade.grade)
        addRating(c, rating)

def exportBook(p, rating, book) :
        c = addNode(p, 'book')
        addText(c, 'isbn', book.isbn)
        addText(c, 'title', book.title)
        addText(c, 'author', personStr(book.author))
        addRating(c, rating)

def exportPaper(p, rating, paper):
        c = addNode(p, 'paper')
        #add journal
        addText(c, 'title', paper.title)
        addText(c, 'author', personStr(paper.author))
        addRating(c, rating)

def exportGame(p, rating, game):
        c = addNode(p, 'game')
        addText(c, 'title', game.title)
        addText(c, 'os', game.platform)
        addRating(c, rating)

def exportPlace(p, rating, place):
        c = addNode(p, nodetypes[type(place)])
        addText(c, 'place_name', place.name)
        addText(c, 'location', str(place.location))
        addText(c, "semester", place.semester + " " + place.year)
        addRating(c, rating)
