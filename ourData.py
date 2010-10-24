from dataAccessors import *

import random

def randString(n):
	alphanum = "abcdefghijklmnopqrstuvwxyz"
	alphanum += alphanum.upper()
	alphanum += "0123456789"
	alphanum += "~!@#$%^&*()-_=+:;/?"
	string = ""
	gen = random.Random()
	for x in range(n):
		string += alphanum[gen.randint(0,len(alphanum)-1)]
	return string
def sidgen():
	return randString(8)
def passgen():
	return randString(12)
	

def main():
	gparker()
	aywang()
	ttb265()
	matt()



def gparker():
	sid = sidgen()
	pwd = passgen()
	me = addStudent(sid,pwd)

	b = addBook("The Good Fairies of New York", "978-0765358547", "Martin Millar")
	addRating(b, me, '100', "Excellent British humor by a lesser know author")
	


def aywang():
	sid = sidgen()
	pwd = passgen()
	me = addStudent(sid,pwd)

def ttb265():
	sid = sidgen()
	pwd = passgen()
	me = addStudent(sid,pwd)
	c = addCourse('52550', 'CS 378', 'Computational Intelligence in Game Design II', 'Fall', '2010', 'Risto Miikkulainen')
	addRating(c, me, '90', 'Interesting research class')
	addGrade(c, me, 'A')
	c = addCourse('52540', 'CS 373', 'Software Engineering', 'Fall', '2010', 'Glenn Downing')
	addRating(c, me, '100', 'Essential.')
	addGrade(c, me, 'B')
	c = addCourse('55480', 'M 346', 'Applied Linear Algebra', 'Fall', '2010', 'Rodriguez-Villegas')
	addRating(c, me, '80', 'Tough class to get a hang of. It really helps if you remember your M 340L material')
	addGrade(c, me, 'B')
	c = addCourse('52435', 'CS 336', 'Analysis of Programs', 'Fall', '2010', 'Margaret Myers')
	addRating(c, me, '90', 'Lecturer is a bit crazy')
	addGrade(c, me, 'B')

	b = addBook("Desperation", "978-0451188465", "Stephen King")
	addRating(b, me, '100', 'Definitely a rainy night page turner');
	addInternship('Center for Teaching and Learning', 'Univ. of Texas', 'Spring', '2010')
	addPlaceStudy('ENS Basement', 'Fall', '2010')
	addPlaceStudy('ENS Basement', 'Fall', '2010')
	addPlaceLive('Ballpark Apartments', 'Fall', '2009')
	addPlaceEat('Big Bite', 'Spring', '2010')
	addPlaceFun('Rain', 'Spring', '2010')
	p = addGame('Atari', 'Tetris')
	addRating(p, me, '100')
	p = addGame( 'Nintento Wii', 'Super Smash Brothers: Brawl')
	addRating(p, me, '90', 'A great game to loosen you up after a long day of classes.')

def matt():
	sid = sidgen()
	pwd = passgen()
	me = addStudent(sid,pwd)
