import unittest
from dataAccessors import *
from dataStore import *
from views import *

class TestView(unittest.TestCase) :
    
    def setUp(self):
        da = DataAccessor()
        a = da.addStudent('ABCDEF', '12345678')
        b = da.addStudent('abcdef', '12345678')
        c = da.addStudent('lololo', 'roflwaff')
        d = da.addStudent('roflwa', 'lollerca')

        course = da.addCourse('12345', 'CS 123', 'Fundamentals of Unit Testing', 'SPRING', '2010', "Unit McUnitson");

        self.course = course;
        da.addRating(course, a, 100)
        da.addRating(course, b, 10)
        da.addRating(course, c, 50)
        da.addRating(course, d, 70)

        da.addGrade(course, a, 'A')
        da.addGrade(course, b, 'B')
        da.addGrade(course, c, 'C')
        da.addGrade(course, d, 'D')
        

    def test_average_rating(self) :
        rating = getAverageRating(self.course)
        self.assertEqual(rating, (57, 4))
         
    def test_rating_class(self) :
        ratingClass = getRatingClass(57)
        self.assertEqual(ratingClass, 'average')
  
    def test_rating_class2(self) :
        ratingClass = getRatingClass(0)
        self.assertEqual(ratingClass, 'bad')
  
    def test_rating_class3(self) :
        ratingClass = getRatingClass(100)
        self.assertEqual(ratingClass, 'good')

    def test_average_grade(self) :
        grade = getAverageGrade(self.course)
        self.assertEqual(grade, 'C+')

    def test_prepare_template(self) :
        out = prepareDataForTemplate(Course.all().filter('unique =', '12345'))

        self.assertEqual(len(out), 1)

        item = out[0]
        self.assertEqual(item.typename, 'Course')

    def test_prepare_template2(self) :
        out = prepareDataForTemplate(Course.all().filter('unique =', '12345'))

        self.assertEqual(len(out), 1)

        item = out[0]
        self.assertEqual(item.rating, 57)
        self.assertEqual(item.ratingCount, 4)
        
    def test_prepare_template3(self) :
        out = prepareDataForTemplate(Course.all().filter('unique =', '12345'))

        self.assertEqual(len(out), 1)

        item = out[0]
        self.assertEqual(item.ratingClass, 'average')   
    
    def test_prepare_template4(self) :
        out = prepareDataForTemplate(Course.all().filter('unique =', '12345'))

        self.assertEqual(len(out), 1)

        item = out[0]
        self.assertEqual(item.avgGrade, 'C+')


