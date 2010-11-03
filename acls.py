import random
import string

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
    return randomString(8)

def passwordGen() : 
    return randomString(12)


def admin(func) : 
    def redirectlogin(self) :
        return self.redirect('/login?msg=Admin%20Login%20Required')

    def checkauth(*args, **kwargs) : 
        self = args[0]
        userkey = self.request.cookies.get('ukey', '')

        if not userkey:
            return redirectlogin(self)

        user = db.get(db.Key(userkey))
        
        if user and user.userType == 'ADMIN' : 
            return func(*args, **kwargs)

        return redirectlogin(self)
    return checkauth

def user(func) : 
    def redirectlogin(self) :
        return self.redirect('/login?msg=Login%20Required')

    def checkauth(*args, **kwargs) : 
        self = args[0]
        userkey = self.request.cookies.get('ukey', '')

        if not userkey:
            return redirectlogin(self)

        user = db.get(db.Key(userkey))

        if user and user.userType == 'STUDENT' : 
            return func(*args, **kwargs)

        return redirectlogin(self)
    return checkauth

