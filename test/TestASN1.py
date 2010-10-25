import unittest
from validators import *
from dataAccessors import *
from google.appengine.ext import db
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
def sidgen():
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
        sid = sidgen()
        pwd = passgen()
        s = da.addStudent(sid,pwd)
        
        db_s = db.get(s)
        self.assertTrue( len(db_s.password) == 12 )
        self.assertTrue( len(db_s.sid) == 8 )
        
    def test_addPaper(self):
        da = DataAccessor()
        p = da.addPaper("conference", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
        
        db_p = db.get(p)
        self.assertTrue( db_p.paperType == 'CONFERENCE' )
        self.assertTrue( db_p.title == 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects' )
        self.assertTrue( db_p.author.fname == 'Chris' )
        self.assertTrue( db_p.author.lname == 'Green' )
    
    def test_addRating(self):
        da = DataAccessor()
        sid = sidgen()
        pwd = passgen()
        s = da.addStudent(sid,pwd)
        p = da.addPaper("conference", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
        r = da.addRating(p, s, '100', "Great paper that explains how Valve used the GPU to render text clearly.")
        
        db_s = db.get(s)
        db_p = db.get(p)
        db_r = db.get(r)
        self.assertTrue( db_r.rater.sid == db_s.sid == sid)
        self.assertTrue( db_r.rater.password == db_s.password == pwd)
        self.assertTrue( db_r.rated.paperType == db_p.paperType == 'conference'.upper())
        self.assertTrue( db_r.rated.title == db_p.title == 'Improved Alpha-Tested Magnification for Vector Textures and Special Effects')
        
        # not complete
        
        
    # Validator Tests
   
    # ---------------
    # uniqueValidator
    # ---------------
        
    def test_uniqueValidator_1(self):
    	try:
    	    uniqueValidator("43213")
    	    self.assertTrue(True)
    	except ValueError:
    		self.assertTrue(False)
    
    def test_uniqueValidator_2(self):
    	try:
    	    uniqueValidator("432133")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    def test_uniqueValidator_3(self):
    	try:
    	    uniqueValidator("1111")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    def test_uniqueValidator_4(self):
    	try:
    	    uniqueValidator("abcde")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    # ------------------
    # courseNumValidator
    # ------------------
    
    def test_courseNumValidator_1(self):
    	try:
    	    courseNumValidator("CS 373")
    	    self.assertTrue(True)
    	except ValueError:
    		self.assertTrue(False)
    
    def test_courseNumValidator_2(self):
    	try:
    	    courseNumValidator("CS 373a")
    	    self.assertTrue(True)
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_courseNumValidator_3(self):
    	try:
    	    courseNumValidator("CS 373aa")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    def test_courseNumValidator_4(self):
    	try:
    	    courseNumValidator("CS373")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    def test_courseNumValidator_5(self):
    	try:
    	    courseNumValidator("CSS 373")
    	    self.assertTrue(True)
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_courseNumValidator_6(self):
    	try:
    	    courseNumValidator("CS 37a")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    def test_courseNumValidator_7(self):
    	try:
    	    courseNumValidator(" 373")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    # --------------
    # gradeValidator
    # --------------
    
    def test_gradeValidator_1(self):
        try:
    	    gradeValidator("")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    def test_gradeValidator_2(self):
        try:
    	    gradeValidator("A+")
    	    self.assertTrue(False)
    	except ValueError:
    		self.assertTrue(True)
    		
    def test_gradeValidator_3(self):
        try:
    	    gradeValidator("A")
    	    self.assertTrue(True)
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_gradeValidator_4(self):
        try:
    	    gradeValidator("B+")
    	    self.assertTrue(True)
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_gradeValidator_5(self):
        try:
    	    gradeValidator("C-")
    	    self.assertTrue(True)
    	except ValueError:
    		self.assertTrue(False)
        
    # -------------
    # yearValidator
    # -------------
    
    def test_yearValidator_1(self):
        self.assertTrue(True)
        
    # -------------
    # isbnValidator
    # -------------
    
    def test_isbnValidator_1(self):
        self.assertTrue(True)
   

if __name__ == '__main__' :
	unittest.main()
