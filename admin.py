from baserequesthandler import BaseRequestHandler
from acls import *
from exporter import export


class AdminPage(BaseRequestHandler) :
    @admin
    def get(self) :
        message = self.request.get('m')
        self.generate('admin.html', {
            'msg' : message, 
            'title' : 'Admin'
        })

    @admin
    def post(self) : 
        self.redirect('/admin')


class AdminExport(BaseRequestHandler) :
    @admin 
    def get(self) : 
        self.generate('export.html', {
            'xml' : export()
            'title' : "Admin Export"})
