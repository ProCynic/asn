#/usr/bin/python

import unittest
from validators import *

class TestASN1(unittest.TestCase):
    """
    """
    def test_addPerson(self):
        self.assertTrue(True)
        
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