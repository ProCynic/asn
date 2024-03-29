"""
"""

import operator
import dataAccessors
from ourExceptions import *
from xml.etree import ElementTree

class Importer:
    def __init__(self, da=dataAccessors.DataAccessor()):
        self.DA = da

    def parse(self, filename):
        """
            Parses the XML file in filename.
        """
        root = ElementTree.parse(filename)
        for student in root.getiterator('student'):
            si = StudentImporter(self.DA)
            si.parse(student)

class StudentImporter:
    def __init__(self, DA):
        self.DA = DA
        self.tags = {'class'        : self.DA.addCourse,
                     'book'         : self.DA.addBook,
                     'paper'        : self.DA.addPaper,
                     'game'         : self.DA.addGame,
                     'live_place'   : self.DA.addPlaceLive,
                     'eat_place'    : self.DA.addPlaceEat,
                     'fun_place'    : self.DA.addPlaceFun,
                     'study_place'  : self.DA.addPlaceStudy,
                     'internship'   : self.DA.addInternship}
        
        self.ptags = {'title'           : lambda x, d: operator.setitem(d, 'title', x.strip()),
                      'author'          : lambda x, d: operator.setitem(d, 'author', x.strip()),
                      'isbn'            : lambda x, d: operator.setitem(d, 'isbn', x.strip().replace('-','')),
                      'paper_category'  : lambda x, d: operator.setitem(d, 'ptype', x.strip()),
                      'unique'          : lambda x, d: operator.setitem(d, 'unique', x.strip()),
                      'course_num'      : lambda x, d: operator.setitem(d, 'num', x.strip()),
                      'course_name'     : lambda x, d: operator.setitem(d, 'name', x.strip()),
                      'instructor'      : lambda x, d: operator.setitem(d, 'instructor', x.strip()),
                      'os'              : lambda x, d: operator.setitem(d, 'platform', x.strip()),
                      'place_name'      : lambda x, d: operator.setitem(d, 'name', x.strip()),
                      'location'        : lambda x, d: operator.setitem(d, 'location', x.strip()),
                      'semester'        : lambda x, d: operator.setitem(d, 'semester', x.strip().split()[0].upper()) or operator.setitem(d, 'year', x.strip().split()[1]),
                      'grade'           : lambda x, d: operator.setitem(d, 'grade', x.strip().upper()),
                      'rating'          : lambda x, d: operator.setitem(d, 'rating', x.strip()),
                      'comment'         : lambda x, d: operator.setitem(d, 'comment', x)}
        
    def parse(self, root):
        """
            Recursively parses the data.
        """
        assert isinstance(root, ElementTree._Element)
        assert root.tag == 'student'
        assert len(root.findall('id')) == 1
        assert len(root.findall('password')) == 1
        sid = root.find('id').text.strip()
        password = root.find('password').text.strip()
        try:
            self.student = self.DA.addStudent(sid, password)

            #will ignore tags not in tag list
            for tag in self.tags:
                for node in root.getiterator(tag):
                    self.parseItem(node)
        except DataStoreClash:
            pass

    def parseItem(self, node):
        """
            Parses a single node in a tree.
        """
        assert node.tag in self.tags
        adder = self.tags[node.tag]
        args = self._getArgs(node)
        rating, comment = self._getRating(args)
        
        grade = None
        if node.tag == 'class':
            try:
                grade = args.pop('grade')
            except KeyError:
                pass

        try:
            x = adder(**args)
            
            self.DA.addRating(x, self.student, rating, comment)

            if grade:
                assert node.tag == 'class'
                self.DA.addGrade(x, self.student, grade)
        except DataStoreClash:
            pass
        except ValueError:
            #bad value
            pass



    def _getArgs(self, node):
        args = {}
        for x in node.getchildren():
            try:
                self.ptags[x.tag](x.text, args)
            except AttributeError:
                pass
        return args

    def _getRating(self, args):
        try:
            rating = args.pop('rating')
        except KeyError:
             Usage("No rating for class")
        try:
            comment = args.pop('comment')
        except KeyError:
            comment = None

        return rating, comment
