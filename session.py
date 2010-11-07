import dataStore as DS
from datetime import *
import hashlib

from google.appengine.ext import db

def __20MinutesFromNow() :
    now = datetime.now()
    minutes = timedelta( minutes = 20 )

    return now + minutes

def sweepSessions() :
    query = DS.Session.all()
    now = datetime.now()
    for x in query :
        if x.expiration > now :
            x.delete()
    

def __invalidateSession(query) :
    for x in query :
        x.delete()

def setSessionMessageByRequest(self, message) :
    setSessionMessage(getSessionByRequest(self), message)


def getSessionByRequest(self) :
    session = getSession(self.request.cookies.get('sid', ''))
    session.expiration = __20MinutesFromNow()
    session.put()
    self.response.headers.add_header(
        'Set-Cookie',
        'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT; path=/' % str(session.sessionID))
    return session

def getSessionMessage(session) :
    message = session.message;
    session.message = None;
    session.put()
    return message

def getSession(sessionID) :
    query = DS.Session.all()

    query.filter('sessionID =', sessionID)

    if (query.count() > 1) :
        __invalidateSessions(query)
        s = generateSession(None)
        setSessionMesage(s, "Duplicate Logins detected")
        return s

    if (query.count() == 0) :
        return generateSession(None)

    session = query.get()
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

    session = DS.Session(sessionID = sid, user = userkey, expiration = __20MinutesFromNow(), generated=False)
    
    session.message = None

    session.put()
    return session

def getSessionUser(session) :
    if (session.user) :
        return session.user;
    return None
