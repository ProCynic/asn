import unittest
from validators import *
from dataAccessors import *
from google.appengine.ext import db

class TestASN1(unittest.TestCase):
        
    # dataAccessors Tests

    def test_addGame(self):
        g = addGame('Atari', 'Tetris')
        
        db_g = db.get(g)
        self.assertTrue( db_g.platform == 'Atari' )
        self.assertTrue( db_g.title == 'Tetris' )
        self.assertFalse( db_g.title == 'Not Tetris' )
        
    def test_addInternship(self):
        i = addInternship('Center for Teaching and Learning', 'Univ. of Texas', 'Spring', '2010')
        
        db_i = db.get(i)
        self.assertTrue( db_i.name == 'Center for Teaching and Learning' )
        self.assertTrue( db_i.location == 'Univ. of Texas' )
        self.assertTrue( db_i.semester == 'SPRING' )
        self.assertTrue( db_i.year == '2010' )
        
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
