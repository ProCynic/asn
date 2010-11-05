import unittest
from dataAccessors import *
from session import *

class TestSession(unittest.TestCase) :
    
    def setUp(self) :
        da = DataAccessor()

        da.addStudent("HIHIHI", "abcdefg")
        self.session = generateSession(42)


    def test_generate(self) :
        other = generateSession(42)

        self.assertTrue(other.sessionID != self.session.sessionID)
