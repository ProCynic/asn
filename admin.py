from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
from dataAccessors import DataAccessor
from session import *

from google.appengine.ext import db

class AdminPage(BaseRequestHandler) :
    @admin
    def get(self) :
        self.generate('admin.html', {
            'title' : 'Admin'
        })

    @admin
    def post(self) : 
        self.redirect('/admin')

class AdminClear(BaseRequestHandler):
    @admin
    def get(self) :
        DA = DataAccessor()
        DA.clear()

        setSessionMessageByRequest(self, "The datastore has been cleared.", False)
        self.redirect('/admin')


class AdminExport(BaseRequestHandler) :
    @admin 
    def get(self) : 
        self.generate('export.html', {
            'xml' : export(),
            'title' : "Admin Export"})


class AdminImport(BaseRequestHandler) :
    def addErrorMessage(self, obj) :
        """
            Callback to show messages
        """

        self.msg += "Duplicate " + str(obj.__class__).strip('<>') + ' ' + str(obj).replace('\n', '<br/>')
        self.msg += "<br/>"

        raise DataStoreClash(obj)

    @admin
    def get(self) :
        setSessionMessageByRequest(self, "Invalid Request", True)
        self.redirect('/admin')
    
    @admin
    def post(self) :
        """
            Does the import, and shows any errors.
        """

        self.msg = ""
        importer = Importer(DataAccessor(self.addErrorMessage))

        try : 
            target = self.request.get('newFile')
            importer.parse(target)

        except IOError :
            self.msg = "Please select a valid file to import"

        except Usage, err : 
            self.msg = err.msg

        if not self.msg : 
            self.msg = 'Import was successful'

        if len(self.msg) > 512 : 
                self.msg = self.msg[0:512] + "..."
        
        setSessionMessageByRequest(self, self.msg)
        self.redirect('/admin')

class ManageUsersPage(BaseRequestHandler) :
    @admin
    def get(self):
        """
        """
        DA = DataAccessor()
        students = DA.getStudents()
        admins = DA.getAdmins()
        self.generate('manageUsers.html', {
            'admins' : admins,
            'students' : students
        })

class UserDel(BaseRequestHandler) :
    @admin
    def get(self, key=None):
        """
        """
        DA = DataAccessor()
        if key == 'all':
            for u in DA.getStudents():
                DA.delete(u)
        elif key:
            user = db.get(db.Key(key))
            DA.delete(user)  
        self.redirect('/admin/manageUsers')

class AdminPassword(BaseRequestHandler) :
    def get(self):
        self.redirect('/admin')
    
    @admin
    def post(self):
        DA = DataAccessor()
        session = getSessionByRequest(self)
        user = getSessionUser(session)
        
        old = self.request.get('old')
        new = self.request.get('new')
        new2 = self.request.get('new2')

        if old != user.password:
            setSessionMessage(session, "Invalid Password")
            self.redirect('/admin')

        if (new != new2) :
            setSessionMessage(session, "Your new passwords did not match. Please try again.", True)
        else:
            setSessionMessage(session, "You have successfully changed your password.", False)
               
            #Reset the password
            DA.update(user, password=new)

            #Reset the session.
            session.generated = False
            session.put()
        self.redirect('/admin')

class CreateAdmin(BaseRequestHandler):
    def get(self):
        self.redirect('/admin')

    @admin
    def post(self):
        DA = DataAccessor()

        session = getSessionByRequest(self)

        uid = self.request.get('uid')
        pw = self.request.get('pw')
        pw2 = self.request.get('pw2')

        if pw != pw2:
            setSessionMessage(session, "Your new passwords did not match. Please try again.", True)
            self.redirect('/admin')

        DA.addAdmin(uid, pw)
        setSessionMessage(session, "Admin: " + uid + " successfully added.", False)
        self.redirect('/admin')
