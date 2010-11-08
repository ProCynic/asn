import dataStore as DS
from datetime import *
import hashlib

from google.appengine.ext import db

def __20MinutesFromNow() :
    now = datetime.now()
    minutes = timedelta( minutes = 20 )

    return now + minutes

def sweepSessions() :
    """
        Kills all sessions that have expired.
    """
    query = DS.Session.all()
    now = datetime.now()
    for x in query :
        if x.expiration > now :
            x.delete()
   
def expireSession(session) :
    """
        Explicitly expire a given session.
    """
    session.delete()

def __invalidateSession(query) : 
    for x in query :
        x.delete()

def setSessionMessageByRequest(self, message, urgent = False) :
    """
        Equivilant to a getSessionByRequest() followed by a setSessionMessage
    """
    setSessionMessage(getSessionByRequest(self), message, urgent)


def getSessionByRequest(self) :
    """
        Given a BaseRequestHandler, returns a session.
    """
    session = getSession(self.request.cookies.get('sid', ''))
    session.expiration = __20MinutesFromNow()
    session.put()
    self.response.headers.add_header(
        'Set-Cookie',
        'sid=%s; expires=Fri, 31-Dec-2020 23:59:59 GMT; path=/' % str(session.sessionID))
    return session

def getSessionMessage(session) :
    """
        Returns the session message, along with its severity as a tuple.
        (message, severity)
    """
    message = session.message;
    session.message = None;
    session.put()
    return message, session.msgstatus

def getSession(sessionID) :
    """
        Gets a session with the given session ID.
        Will generate a session if no such session exists, and will
        expire sessions if a key will clash.
    """
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

def setSessionMessage(session, msg, urgent = False) :
    """
        Sets the session message.
    """
    session.message = msg;
    session.msgstatus = urgent;
    session.put()

def generateSession(userkey) : 
    """
        Generates a new session with the given user.
        If user is None, then this is a browser session.
    """
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
    """
        Returns the session's user, if applicable.
    """
    if (session.user) :
        return session.user;
    return None
