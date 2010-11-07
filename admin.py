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

        setSessionMessageByRequest(self, "The datastore has been cleared.")
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
        setSessionMessageByRequest(self, "Invalid Request")
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
        
