from dataAccessors import DataAccessor

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
        DA = DataAccessor()
	gparker(DA)
	aywang(DA)
	ttb265(DA)
	matt(DA)



def gparker(DA):
	sid = sidgen()
	pwd = passgen()
	me = DA.addStudent(sid,pwd)

	b = DA.addBook("The Good Fairies of New York", "978-0765358547", "Martin Millar")
	DA.addRating(b, me, '100', "Excellent British humor by a lesser know author")

	e = DA.addPlaceEat("EZ's", "3918 N Lamar Blvd Austin, TX 78756-4017", "FALL", "2010")
	DA.addRating(e, me, '85', "Decent food.  They've got a student discount: $2 off on $7 or more")

	g = DA.addGame("PC","Minecraft")
	DA.addRating(g, me, "100", 
	
	


def aywang(DA):
	sid = sidgen()
	pwd = passgen()
	me = DA.addStudent(sid,pwd)

	b = DA.addBook("Dune, 40th Anniversary Edition (Dune Chronicles, Book 1)", "0441013597", "Frank Herbert")
	DA.addRating(b, me, '90', "Great book, but the sequels are kinda poor.")

	b = DA.addCourse("52540", "C S 375", "Software Engineering", "Fall", "2010", "Glen Downing")
	DA.addRating(b, me, '75', "Fun assignments, but the class itself bores me.")
	DA.addGrade(b, me, 'A')
	
	b = DA.addPaper("conference", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
	DA.addRating(b, me, '100', "Great paper that explains how Valve used the GPU to render text clearly.")

	b = DA.addGame("Xbox360", "Blazblue: Continumn Shift")
	DA.addRating(b, me, '80', "Great fighter game, sometimes lags online.")

	b = DA.addPlaceLive("Duval Villas", "4305 Duval St." "Fall", "2009")
	DA.addRating(b, me, '30', "A bit expensive for what you get.")

	b = DA.addPlaceEat('The Ironworks', '100 Red River St.', "Fall", "2010")
	DA.addRating(b, me, '100', "I love eating here, the beef ribs are delicious.")

	b = DA.addPlaceFun('Arcade UFO', '3101 Speedway', "Fall", "2010")
	DA.addRating(b, me, '80', "Great arcade place in Austin, one of the few left.")

	b = DA.addPlaceStudy('ENS Labs', 'ENS Basement', "Fall", "2010")
	DA.addRating(b, me, '86', "No taylor basement, but its still filled with intelligent people to help.")

def ttb265(DA):
	sid = sidgen()
	pwd = passgen()
	me = DA.addStudent(sid,pwd)
	c = DA.addCourse('52550', 'CS 378', 'Computational Intelligence in Game Design II', 'Fall', '2010', 'Risto Miikkulainen')
	DA.addRating(c, me, '90', 'Interesting research class')
	DA.addGrade(c, me, 'A')
	c = DA.addCourse('52540', 'CS 373', 'Software Engineering', 'Fall', '2010', 'Glenn Downing')
	DA.addRating(c, me, '100', 'Essential.')
	DA.addGrade(c, me, 'B')
	c = DA.addCourse('55480', 'M 346', 'Applied Linear Algebra', 'Fall', '2010', 'Rodriguez-Villegas')
	DA.addRating(c, me, '80', 'Tough class to get a hang of. It really helps if you remember your M 340L material')
	DA.addGrade(c, me, 'B')
	c = DA.addCourse('52435', 'CS 336', 'Analysis of Programs', 'Fall', '2010', 'Margaret Myers')
	DA.addRating(c, me, '90', 'Lecturer is a bit crazy')
	DA.addGrade(c, me, 'B')

	b = DA.addBook("Desperation", "978-0451188465", "Stephen King")
	DA.addRating(b, me, '100', 'Definitely a rainy night page turner');
	DA.addInternship('Center for Teaching and Learning', 'Univ. of Texas', 'Spring', '2010')
	DA.addPlaceStudy('ENS Basement', 'Fall', '2010')
	DA.addPlaceStudy('ENS Basement', 'Fall', '2010')
	DA.addPlaceLive('Ballpark Apartments', 'Fall', '2009')
	DA.addPlaceEat('Big Bite', 'Spring', '2010')
	DA.addPlaceFun('Rain', 'Spring', '2010')
	g = DA.addGame('Atari', 'Tetris')
	DA.addRating(p, me, '100')
	g = DA.addGame( 'Nintento Wii', 'Super Smash Brothers: Brawl')
	DA.addRating(p, me, '90', 'A great game to loosen you up after a long day of classes.')

def matt(DA):
	sid = sidgen()
	pwd = passgen()
	me = DA.addStudent(sid,pwd)


main()
