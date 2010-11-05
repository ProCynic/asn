import unittest
from dataAccessors import *
from session import *
from datetime import *
from dataStore import *

class TestSession(unittest.TestCase) :
    
    def setUp(self) :
        da = DataAccessor()

        self.user = da.addStudent("HIHIHI", "abcdefg")
        self.user2 = da.addStudent("BYEBYE", "asdfjkl;")
        self.session = generateSession(self.user)
        self.session2 = generateSession(self.user2)


    def test_generate(self) :
        self.assertTrue(self.session.sessionID != self.session2.sessionID)

    def test_message(self) :
        setSessionMessage(self.session, "Test")
        self.assertEqual(getSessionMessage(self.session), "Test")
        self.assertEqual(getSessionMessage(self.session), None)

    def test_expire(self) :
        sid = self.session2.sessionID
        self.session2.expiration = datetime.now()
        sweepSessions()

        count = Session.all().filter('sessionID = ', sid).count()
        self.assertEqual(count, 0)
