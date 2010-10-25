import unittest
from validators import *

class TestValidators(unittest.TestCase):
    """
    """
    # ---------------
    # uniqueValidator
    # ---------------
        
    def test_uniqueValidator_1(self):
    	try:
    	    uniqueValidator("43213")
    	except ValueError:
    		self.assertTrue(False)
    
    def test_uniqueValidator_2(self):
    	self.assertRaises(ValueError, uniqueValidator, "432133")
    		
    def test_uniqueValidator_3(self):
    	self.assertRaises(ValueError, uniqueValidator, "1111")
    		
    def test_uniqueValidator_4(self):
    	self.assertRaises(ValueError, uniqueValidator, "abcde")
    		
    # ------------------
    # courseNumValidator
    # ------------------
    
    def test_courseNumValidator_1(self):
    	try:
    	    courseNumValidator("CS 373")
    	except ValueError:
    		self.assertTrue(False)
    
    def test_courseNumValidator_2(self):
    	try:
    	    courseNumValidator("CS 373a")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_courseNumValidator_3(self):
    	self.assertRaises(ValueError, courseNumValidator, "CS 373aa")
    		
    def test_courseNumValidator_4(self):
    	self.assertRaises(ValueError, courseNumValidator, "CS373")
    		
    def test_courseNumValidator_5(self):
    	try:
    	    courseNumValidator("CSS 373")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_courseNumValidator_6(self):
    	self.assertRaises(ValueError, courseNumValidator, "CS 37a")
    		
    def test_courseNumValidator_7(self):
    	self.assertRaises(ValueError, courseNumValidator, " 373")
    		
    # --------------
    # gradeValidator
    # --------------
    
    def test_gradeValidator_1(self):
        self.assertRaises(ValueError, gradeValidator, "")
    		
    def test_gradeValidator_2(self):
       self.assertRaises(ValueError, gradeValidator, "A+")
    		
    def test_gradeValidator_3(self):
        try:
    	    gradeValidator("A")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_gradeValidator_4(self):
        try:
    	    gradeValidator("B+")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_gradeValidator_5(self):
        try:
    	    gradeValidator("C-")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_gradeValidator_6(self):
        self.assertRaises(ValueError, gradeValidator, "C--")
        
    def test_gradeValidator_7(self):
        self.assertRaises(ValueError, gradeValidator, "D++")
        
    def test_gradeValidator_8(self):
        self.assertRaises(ValueError, gradeValidator, "AA")
        
    # -------------
    # yearValidator
    # -------------
    
    def test_yearValidator_1(self):
        try:
    	    yearValidator("1974")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_yearValidator_2(self):
        self.assertRaises(ValueError, yearValidator, "198A")
       
    def test_yearValidator_3(self):
        self.assertRaises(ValueError, yearValidator, "19873")
        
    def test_yearValidator_4(self):
        self.assertRaises(ValueError, yearValidator, "198")
        
    # -------------
    # isbnValidator
    # -------------
    
    def test_isbnValidator_1(self):
        try:
    	    isbnValidator("1594202664")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_isbnValidator_2(self):
        try:
    	    isbnValidator("9781594202667")
    	except ValueError:
    		self.assertTrue(False)
    		
    def test_isbnValidator_3(self):
        self.assertRaises(ValueError, isbnValidator, "1234567890")
        
    def test_isbnValidator_4(self):
        self.assertRaises(ValueError, isbnValidator, "1231234567890")
    
    def test_isbnValidator_5(self):
        self.assertRaises(ValueError, isbnValidator, "")
        
    def test_isbnValidator_6(self):
        self.assertRaises(ValueError, isbnValidator, "11111111111111")
   

if __name__ == '__main__' :
	unittest.main()
