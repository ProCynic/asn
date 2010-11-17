import random
import string

from session import *


from google.appengine.ext import db


def __randomString(length) : 
	characters =  "abcdefghijklmnopqrstuvwxyz"
	characters += "ABCDEFGHIJKLMNOPQRSTUVWXZY"
	characters += "0123456789"

	generator = random.Random()
	
	string = ""
	for x in range(length) :
		string += characters[generator.randint(0, len(characters) - 1)];
	return string


def userIDGen() : 
	"""
		Returns a randomly generated UserID.
	"""
	return __randomString(8)

def passwordGen() : 
	"""
		Returns a randomly generated password.
	"""
	return __randomString(12)

def admin(func) : 
    """
    This function is used as a decorator on the pages.
    Any user attempting to access admin protected pages will be 
    redirected to the login page if they are not an admin.
    """
    def redirectlogin(session, self) :
        setSessionMessage(session, "Admin Login Required.", True)
        return self.redirect('/login')

    def checkauth(*args, **kwargs) : 
        self = args[0]

                           
        session = getSessionByRequest(self)
        user = getSessionUser(session)

        if not user :
                return redirectlogin(session, self)

        if user.userType == 'ADMIN' : 
                return func(*args, **kwargs)

        return redirectlogin(session, self)
    return checkauth

def user(func) : 
    """
    This function is used as a decorator on the pages.
    Any user attempting to access student protected pages will be 
    redirected to the login page if they are not an student.
    """
    def redirectlogin(session, self) :
        setSessionMessage(session, "Student Login required", True)
        return self.redirect('/login')

    def checkauth(*args, **kwargs) : 
        self = args[0]
        session = getSessionByRequest(self)
        user = getSessionUser(session)

        if not user :
            return redirectlogin(session, self)

        if user.userType == 'STUDENT' : 
            return func(*args, **kwargs)

        return redirectlogin(session, self)
    return checkauth

