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

        da.addRating(course, a, 100)
        da.addRating(course, b, 10)
        da.addRating(course, c, 50)
        da.addRating(course, d, 70)

        da.addGrade(course, a, 'A')
        da.addGrade(course, b, 'B')
        da.addGrade(course, c, 'C')
        da.addGrade(course, d, 'D')
        

    def test_average_rating(self) :
        course = Course.all().filter('unique =', '12345');
        self.assertEqual(course.count(), 1)
        rating = getAverageRating(course.get())
        self.assertEqual(rating, (57.5, 4))
         

