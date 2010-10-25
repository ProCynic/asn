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

	b = addBook("Dune, 40th Anniversary Edition (Dune Chronicles, Book 1)", "0441013597", "Frank Herbert")
	addRating(b, me, '90', "Great book, but the sequels are kinda poor.")

	b = addCourse("52540", "C S 375", "Software Engineering", "Fall", "2010", "Glen Downing")
	addRating(b, me, '75', "Fun assignments, but the class itself bores me.")
	addGrade(b, me, 'A')
	
	b = addPaper("conference", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
	addRating(b, me, '100', "Great paper that explains how Valve used the GPU to render text clearly.")

	b = addGame("Xbox360", "Blazblue: Continumn Shift")
	addRating(b, me, '80', "Great fighter game, sometimes lags online.")

	b = addPlaceLive("Duval Villas", "4305 Duval St." "Fall", "2009")
	addRating(b, me, '30', "A bit expensive for what you get.")

	b = addPlaceEat('The Ironworks', '100 Red River St.', "Fall", "2010")
	addRating(b, me, '100', "I love eating here, the beef ribs are delicious.")

	b = addPlaceFun('Arcade UFO', '3101 Speedway', "Fall", "2010")
	addRating(b, me, '80', "Great arcade place in Austin, one of the few left.")

	b = addPlaceStudy('ENS Labs', 'ENS Basement', "Fall", "2010")
	addRating(b, me, '86', "No taylor basement, but its still filled with intelligent people to help.")

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
	g = addGame('Atari', 'Tetris')
	addRating(p, me, '100')
	g = addGame( 'Nintento Wii', 'Super Smash Brothers: Brawl')
	addRating(p, me, '90', 'A great game to loosen you up after a long day of classes.')

def matt():
	sid = sidgen()
	pwd = passgen()
	me = addStudent(sid,pwd)
