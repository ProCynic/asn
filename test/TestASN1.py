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
        
        db_g = db.get(g)
        self.assertTrue( db_g.platform == 'Atari' )
        self.assertTrue( db_g.title == 'Tetris' )
        self.assertFalse( db_g.title == 'Not Tetris' )
        
    def test_addInternship(self):
        da = DataAccessor()
        i = da.addInternship('Center for Teaching and Learning', 'Univ. of Texas', 'Spring'.upper(), '2010')
        
        db_i = db.get(i)
        self.assertTrue( db_i.name == 'Center for Teaching and Learning' )
        self.assertTrue( db_i.location == 'Univ. of Texas' )
        self.assertTrue( db_i.semester == 'SPRING' )
        self.assertTrue( db_i.year == '2010' )
        
    def test_addStudent(self):
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        
        db_s = db.get(s)
        self.assertTrue( len(db_s.password) == 12 )
        self.assertTrue( len(db_s.uid) == 8 )
        
    def test_addPaper(self):
        da = DataAccessor()
        p = da.addPaper("CONFERENCE", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
        
        db_p = db.get(p)
        self.assertTrue( db_p.paperType == 'CONFERENCE' )
        self.assertTrue( db_p.title == 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects' )
        self.assertTrue( db_p.author.fname == 'Chris' )
        self.assertTrue( db_p.author.lname == 'Green' )
    
    def test_addRating(self):
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        p = da.addPaper("CONFERENCE", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
        r = da.addRating(p, s, '100', "Great paper that explains how Valve used the GPU to render text clearly.")
        
        db_s = db.get(s)
        db_p = db.get(p)
        db_r = db.get(r)
        self.assertTrue( db_r.rater.uid == db_s.uid == uid)
        self.assertTrue( db_r.rater.password == db_s.password == pwd)
        self.assertTrue( db_r.rated.paperType == db_p.paperType == 'conference'.upper())
        self.assertTrue( db_r.rated.title == db_p.title == 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects')
        self.assertTrue( db_r.rated.author.fname == db_p.author.fname == 'Chris')
        self.assertTrue( db_r.rated.author.lname == db_p.author.lname == 'Green')
        self.assertTrue( db_r.rating == 100)
        self.assertTrue( db_r.comment.text == 'Great paper that explains how Valve used the GPU to render text clearly.')
        
    def test_addPlaceLive(self):
        da = DataAccessor()
        p = da.addPlaceLive('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        db_p = db.get(p)
        self.assertTrue( db_p.name == 'Ballpark Apartments')
        self.assertTrue( db_p.location == 'Univ. of Texas')
        self.assertTrue( db_p.semester == 'FALL')
        self.assertTrue( db_p.year == '2009')
        
    def test_addPlaceEat(self):
        da = DataAccessor()
        p = da.addPlaceEat('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        db_p = db.get(p)
        self.assertTrue( db_p.name == 'Ballpark Apartments')
        self.assertTrue( db_p.location == 'Univ. of Texas')
        self.assertTrue( db_p.semester == 'FALL')
        self.assertTrue( db_p.year == '2009')
        
    def test_addPlaceFun(self):
        da = DataAccessor()
        p = da.addPlaceFun('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        db_p = db.get(p)
        self.assertTrue( db_p.name == 'Ballpark Apartments')
        self.assertTrue( db_p.location == 'Univ. of Texas')
        self.assertTrue( db_p.semester == 'FALL')
        self.assertTrue( db_p.year == '2009')
        
    def test_addPlaceStudy(self):
        da = DataAccessor()
        p = da.addPlaceStudy('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        db_p = db.get(p)
        self.assertTrue( db_p.name == 'Ballpark Apartments')
        self.assertTrue( db_p.location == 'Univ. of Texas')
        self.assertTrue( db_p.semester == 'FALL')
        self.assertTrue( db_p.year == '2009')
        
    def test_addInternship(self):
        da = DataAccessor()
        p = da.addInternship('Ballpark Apartments', 'Univ. of Texas', 'Fall'.upper(), '2009')
        
        db_p = db.get(p)
        self.assertTrue( db_p.name == 'Ballpark Apartments')
        self.assertTrue( db_p.location == 'Univ. of Texas')
        self.assertTrue( db_p.semester == 'FALL')
        self.assertTrue( db_p.year == '2009')
        
    def test_addCourse(self):
        da = DataAccessor()
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        c = da.addCourse('52540', 'CS 373', 'Software Engineering', 'Fall'.upper(), '2010', 'Glenn Downing')
        
        db_s = db.get(s)
        db_c = db.get(c)
        self.assertTrue( db_c.unique == '52540')
        self.assertTrue( db_c.courseNum == 'CS 373')
        self.assertTrue( db_c.name == 'Software Engineering')
        self.assertTrue( db_c.semester == 'FALL')
        self.assertTrue( db_c.instructor.fname == 'Glenn')
        self.assertTrue( db_c.instructor.lname == 'Downing')
        self.assertTrue( db_c.year == '2010')
        self.assertTrue( db_s.uid == uid)
        self.assertTrue( db_s.password == pwd)
        
    def test_addGrade(self):
        da = DataAccessor()
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        c = da.addCourse('52540', 'CS 373', 'Software Engineering', 'Fall'.upper(), '2010', 'Glenn Downing')
        g = da.addGrade(c, s, 'B')
        
        db_s = db.get(s)
        db_c = db.get(c)
        db_g = db.get(g)
        self.assertTrue( db_g.course.unique == db_c.unique == '52540')
        self.assertTrue( db_g.course.courseNum == db_c.courseNum == 'CS 373')
        self.assertTrue( db_g.course.name == db_c.name == 'Software Engineering')
        self.assertTrue( db_g.course.semester == db_c.semester == 'FALL')
        self.assertTrue( db_g.course.instructor.fname == db_c.instructor.fname == 'Glenn')
        self.assertTrue( db_g.course.instructor.lname == db_c.instructor.lname == 'Downing')
        self.assertTrue( db_g.course.year == db_c.year == '2010')
        self.assertTrue( db_g.student.uid == db_s.uid == uid)
        self.assertTrue( db_g.student.password == db_s.password == pwd)
        self.assertTrue( db_g.grade == 'B')
        
    def test_deleteRatable(self):
    	da = DataAccessor()
        da = DataAccessor()
        uid = uidgen()
        pwd = passgen()
        s = da.addStudent(uid,pwd)
        p = da.addPaper("CONFERENCE", "Test Paper", "Chris Brown")
        r = da.addRating(p, s, '100', "Great paper that explains how Valve used the GPU to render text clearly.")
        
        self.assertTrue(db.get(p))
        self.assertTrue(db.get(r))
        
        db_p = db.get(p)
        
        da.delete(db_p)
        
        self.assertFalse(db.get(p))
        self.assertFalse(db.get(r))

if __name__ == '__main__' :
	unittest.main()
