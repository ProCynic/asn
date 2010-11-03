import dataStore as DS
from datetime import *
import hashlib

from google.appengine.ext import db

def __20MinutesFromNow() :
    now = datetime.now()
    minutes = timedelta( minutes = 20 )

    return now + minutes

def sweepSessions() :
    pass

def invalidateSession(sid) :
    pass

def getSessionByRequest(self) :
    session = getSession(self.request.cookies.get('sid', ''))
    return session

def getSession(sessionID) :
    query = DS.Session.all()

    query.filter('sessionID =', sessionID)

    if (query.count() > 1) :
        invalidateSession(sessionID)
        return generateSession(None)

    if (query.count() == 0) :
        return generateSession(None)

    return query.get()

def setSessionMessage(session, msg) :
    session.message = msg;
    session.put()

def generateSession(userkey) : 
    #Generate a secure session ID
    h = hashlib.md5()
    h.update(str(userkey))
    h.update(str(datetime.now()))
    h.update(str("This is the secret hash zomg"))


    sid = h.hexdigest()
   
    session = DS.Session(sessionID = sid, user = userkey, expiration = __20MinutesFromNow())
    
    session.message = None

    session.put()
    return session

def getSessionUser(session) :
    if (session.user) :
        return session.user;
    return None
