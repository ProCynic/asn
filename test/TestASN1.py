import unittest

class TestASN1(unittest.TestCase):
    """
    """

from dataAccessors import *
from google.appengine.ext import db
from ourExceptions import *
import random

def randString(n):
	alphanum = "abcdefghijklmnopqrstuvwxyz"
	alphanum += alphanum.upper()
	alphanum += "0123456789"
	alphanum += "~!@#$%^&*()-_=+:;/?"
	string = ""
	gen = random.Random()
	for x in range(n):
		string += alphanum[gen.randint(0,len(alphanum)-1)]
	return string
def uidgen():
	return randString(8)
def passgen():
	return randString(12)

class TestASN1(unittest.TestCase):

    # dataAccessors Tests

    def test_addGame(self):
        da = DataAccessor()
        g = da.addGame('Atari', 'Tetris')
        
        self.assertTrue( g.platform == 'Atari' )
        self.assertTrue( g.title == 'Tetris' )
        self.assertFalse( g.title == 'Not Tetris' )
        
    def test_addInternship(self):
        da = DataAccessor()
        i = da.addInternship('Center for Teaching and Learning', 'Univ. of Texas', 'Spring'.upper(), '2010')
        
        self.assertTrue( i.name == 'Center for Teaching and Learning' )
        self.assertTrue( i.location == 'Univ. of Texas' )
        self.assertTrue( i.semester == 'SPRING' )
        self.assertTrue( i.year == '2010' )
        
    def test_addStudent(self):
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        
        self.assertTrue( len(s.password) == 12 )
        self.assertTrue( len(s.uid) == 8 )
        
    def test_addPaper(self):
        da = DataAccessor()
        p = da.addPaper("CONFERENCE", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
        
        self.assertTrue( p.paperType == 'CONFERENCE' )
        self.assertTrue( p.title == 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects' )
        self.assertTrue( p.author.fname == 'Chris' )
        self.assertTrue( p.author.lname == 'Green' )
    
    def test_addRating(self):
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        p = da.addPaper("CONFERENCE", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
        r = da.addRating(p, s, '100', "Great paper that explains how Valve used the GPU to render text clearly.")
        
        self.assertTrue( r.rater.uid == s.uid == uid)
        self.assertTrue( r.rater.password == s.password == pwd)
        self.assertTrue( r.rated.paperType == p.paperType == 'conference'.upper())
        self.assertTrue( r.rated.title == p.title == 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects')
        self.assertTrue( r.rated.author.fname == p.author.fname == 'Chris')
        self.assertTrue( r.rated.author.lname == p.author.lname == 'Green')
        self.assertTrue( r.rating == 100)
        self.assertTrue( r.comment.text == 'Great paper that explains how Valve used the GPU to render text clearly.')
        
    def test_addPlaceLive(self):
        da = DataAccessor()
        p = da.addPlaceLive('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        self.assertTrue( p.name == 'Ballpark Apartments')
        self.assertTrue( p.location == 'Univ. of Texas')
        self.assertTrue( p.semester == 'FALL')
        self.assertTrue( p.year == '2009')
        
    def test_addPlaceEat(self):
        da = DataAccessor()
        p = da.addPlaceEat('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        self.assertTrue( p.name == 'Ballpark Apartments')
        self.assertTrue( p.location == 'Univ. of Texas')
        self.assertTrue( p.semester == 'FALL')
        self.assertTrue( p.year == '2009')
        
    def test_addPlaceFun(self):
        da = DataAccessor()
        p = da.addPlaceFun('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        self.assertTrue( p.name == 'Ballpark Apartments')
        self.assertTrue( p.location == 'Univ. of Texas')
        self.assertTrue( p.semester == 'FALL')
        self.assertTrue( p.year == '2009')
        
    def test_addPlaceStudy(self):
        da = DataAccessor()
        p = da.addPlaceStudy('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        self.assertTrue( p.name == 'Ballpark Apartments')
        self.assertTrue( p.location == 'Univ. of Texas')
        self.assertTrue( p.semester == 'FALL')
        self.assertTrue( p.year == '2009')
        
    def test_addInternship(self):
        da = DataAccessor()
        p = da.addInternship('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        self.assertTrue( p.name == 'Ballpark Apartments')
        self.assertTrue( p.location == 'Univ. of Texas')
        self.assertTrue( p.semester == 'FALL')
        self.assertTrue( p.year == '2009')
        
    def test_addCourse(self):
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        c = da.addCourse('52540', 'CS 373', 'Software Engineering', 'Fall'.upper(), '2010', 'Glenn Downing')
        
        self.assertTrue( c.unique == '52540')
        self.assertTrue( c.courseNum == 'CS 373')
        self.assertTrue( c.name == 'Software Engineering')
        self.assertTrue( c.semester == 'FALL')
        self.assertTrue( c.instructor.fname == 'Glenn')
        self.assertTrue( c.instructor.lname == 'Downing')
        self.assertTrue( c.year == '2010')
        self.assertTrue( s.uid == uid)
        self.assertTrue( s.password == pwd)
        
    def test_addGrade(self):
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        c = da.addCourse('52540', 'CS 373', 'Software Engineering', 'Fall'.upper(), '2010', 'Glenn Downing')
        g = da.addGrade(c, s, 'B')
        
        self.assertTrue( g.course.unique == c.unique == '52540')
        self.assertTrue( g.course.courseNum == c.courseNum == 'CS 373')
        self.assertTrue( g.course.name == c.name == 'Software Engineering')
        self.assertTrue( g.course.semester == c.semester == 'FALL')
        self.assertTrue( g.course.instructor.fname == c.instructor.fname == 'Glenn')
        self.assertTrue( g.course.instructor.lname == c.instructor.lname == 'Downing')
        self.assertTrue( g.course.year == c.year == '2010')
        self.assertTrue( g.student.uid == s.uid == uid)
        self.assertTrue( g.student.password == s.password == pwd)
        self.assertTrue( g.grade == 'B')
        
    def test_deleteRatable(self):
    	da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        p = da.addPaper("CONFERENCE", "Test Paper", "Chris Brown")
        r = da.addRating(p, s, '100', "Great paper that explains how Valve used the GPU to render text clearly.")
        
        self.assertTrue(p.is_saved())
        self.assertTrue(r.is_saved())

        da.delete(p)
        
        self.assertFalse(db.get(p.key()))
        self.assertFalse(db.get(r.key()))

if __name__ == '__main__' :
	unittest.main()
