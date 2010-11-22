from baserequesthandler import BaseRequestHandler

from acls import *
from exporter import export
from ourExceptions import *
from importer import Importer 
from dataAccessors import DataAccessor
from session import *

from google.appengine.ext import db
from StringIO import StringIO

class AdminPage(BaseRequestHandler) :
    """
        The base admin page. This is the main
        interface for administrative tasks.
    """
    @admin
    def get(self) :
        """
            Generate the interface.
        """
        self.generate('admin.html', {
            'title' : 'Admin'
        })

    @admin
    def post(self) : 
        """
            This method should not be accessed.
            Any attempt to do so will be redirected to the GET page.
        """
        self.redirect('/admin')

class AdminClear(BaseRequestHandler):
    """
        Controller for the Clear command.
    """
    @admin
    def get(self) :
        """
            Clears the datastore on access.
        """
        DA = DataAccessor()
        DA.clear()

        setSessionMessageByRequest(self, "The datastore has been cleared.", False)
        self.redirect('/admin')


class AdminExport(BaseRequestHandler) :
    """
        Controller for the export command.
    """
    @admin 
    def get(self) : 
        """
            Generate a page with XML in a textarea for copy paste.
        """
        self.generate('export.html', {
            'xml' : export(),
            'title' : "Admin Export"})


class AdminImport(BaseRequestHandler) :
    """
        Controller for Importing things.
    """
    def addErrorMessage(self, obj) :
        """
            Callback to show messages
        """

        self.msg += "Duplicate " + str(obj.__class__).strip('<>') + ' ' + str(obj).replace('\n', '<br/>')
        self.msg += "<br/>"

        raise DataStoreClash(obj)

    @admin
    def get(self) :
        """
            Should not be accessed. Any attempt will be redirected
            to the base admin page.
        """
        setSessionMessageByRequest(self, "Invalid Request", True)
        self.redirect('/admin')
    
    @admin
    def post(self) :
        """
            Does the import, and shows any errors.
        """

        self.msg = ""
        error = True
        importer = Importer(DataAccessor(self.addErrorMessage))

        try : 
            target = self.request.POST.get('newFile').file.read()
            importer.parse(StringIO(target))

        except IOError :
            self.msg = "Please select a valid file to import"

        except Usage, err : 
            self.msg = err.msg

        if not self.msg : 
            self.msg = 'Import was successful'
            error = False

        if len(self.msg) > 512 : 
                self.msg = self.msg[0:512] + "..."
        
        setSessionMessageByRequest(self, self.msg, error)
        self.redirect('/admin')

class ManageUsersPage(BaseRequestHandler) :
    """
        Controller for managing users.
    """
    @admin
    def get(self):
        """
            Will generate the user management page.
        """
        DA = DataAccessor()
        students = DA.getStudents()
        admins = DA.getAdmins()
        self.generate('manageUsers.html', {
            'admins' : admins,
            'students' : students
        })

class UserDel(BaseRequestHandler) :
    """
        Controller for deleting users.
    """
    @admin
    def get(self, key=None):
        """
            Deletes the user in question.
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
    """
        Controller for changing the admin password.
    """
    @admin
    def get(self):
        """
            Should not be accessed. Any attempt to 
            will be redirected to the base admin page.
        """
        self.redirect('/admin')
    
    @admin
    def post(self):
        """
            Changes the admin password.
        """
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
    """
        Controller for creating an admin"
    """
    def get(self):
        """
            Does nothing but redirect to the root admin page.
        """
        self.redirect('/admin')

    @admin
    def post(self):
        """
            Creates a new admin. Required post request parameters are
                uid - the new user id
                pw - the new password
                pw2 - retyping the new password.
        """
        DA = DataAccessor()

        session = getSessionByRequest(self)

        uid = self.request.get('uid')
        pw = self.request.get('pw')
        pw2 = self.request.get('pw2')

        if pw != pw2:
            setSessionMessage(session, "Your new passwords did not match. Please try again.", True)
            self.redirect('/admin')
            return

        try:
            DA.addAdmin(uid, pw)
        except Usage:
            setSessionMessage(session, "A user with that uid exists already", True)
            self.redirect('/admin')
            return
        
        setSessionMessage(session, "Admin: " + uid + " successfully added.", False)
        self.redirect('/admin')
