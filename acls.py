import random
import string

from session import *


from google.appengine.ext import db


def __randomString(length) : 
    characters =  "abcdefghijklmnopqrstuvwxyz"
    characters += "ABCDEFGHIJKLMNOPQRSTUVWXZY"
    characters += "0123456789"
    characters += "~!@#$%^&*()_+-=:;/?"

    generator = random.Random()
    
    string = ""
    for x in range(length) :
        string += characters[generator.randint(0, len(characters) - 1)];
    return string


def userIDGen() : 
    return __randomString(8)

def passwordGen() : 
    return __randomString(12)

def admin(func) : 
    def redirectlogin(session, self) :
        setSessionMessage(session, "Admin Login Required.", False)
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
    def redirectlogin(session, self) :
        setSessionMessage(session, "Student Login required", False)
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

