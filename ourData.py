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
	

def nullErrorHandler(x) :
	pass

def main():
	DA = DataAccessor(nullErrorHandler)
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
	DA.addRating(g, me, "100", "Excellent Robinson Crusoe simulator.  Start with nothing and build whatever you want.")

	b = DA.addBook("Island in the Sea of Time", "978-0451456755", "S.M. Stirling")
	DA.addRating(b, me, '90')

	b = DA.addBook("On Basilisk Station", "978-0743435710", "David Weber")
	DA.addRating(b, me, '97', "The Start of an excellent series")

	c = DA.addCourse("52540", "CS 373", "Software Engineering", "FALL", "2010", "Glen Downing")
	DA.addRating(c, me, '80', "Assignments are interesting")

	
	

	
	
	


def aywang(DA):
	sid = sidgen()
	pwd = passgen()
	me = DA.addStudent(sid,pwd)

	b = DA.addBook("Dune, 40th Anniversary Edition (Dune Chronicles, Book 1)", "0441013597", "Frank Herbert")
	DA.addRating(b, me, '90', "Great book, but the sequels are kinda poor.")

	b = DA.addCourse("52540", "CS 373", "Software Engineering", "FALL", "2010", "Glen Downing")
	DA.addRating(b, me, '75', "Fun assignments, but the class itself bores me.")
	DA.addGrade(b, me, 'A')
	
	b = DA.addPaper("conference", "Improved Alpha-Tested Magnification for Vector Textures and Special Effects", "Chris Green")
	DA.addRating(b, me, '100', "Great paper that explains how Valve used the GPU to render text clearly.")

	b = DA.addGame("Xbox360", "Blazblue: Continumn Shift")
	DA.addRating(b, me, '80', "Great fighter game, sometimes lags online.")

	b = DA.addPlaceLive("Duval Villas", "4305 Duval St.", "FALL", "2009")
	DA.addRating(b, me, '30', "A bit expensive for what you get.")

	b = DA.addPlaceEat('The Ironworks', '100 Red River St.', "FALL", "2010")
	DA.addRating(b, me, '100', "I love eating here, the beef ribs are delicious.")

	b = DA.addPlaceFun('Arcade UFO', '3101 Speedway', "FALL", "2010")
	DA.addRating(b, me, '80', "Great arcade place in Austin, one of the few left.")

	b = DA.addPlaceStudy('ENS Labs', 'ENS Basement', "FALL", "2010")
	DA.addRating(b, me, '86', "No taylor basement, but its still filled with intelligent people to help.")

def ttb265(DA):
	sid = sidgen()
	pwd = passgen()
	me = DA.addStudent(sid,pwd)
	c = DA.addCourse('52550', 'CS 378', 'Computational Intelligence in Game Design II', 'FALL', '2010', 'Risto Miikkulainen')
	DA.addRating(c, me, '90', 'Interesting research class')
	DA.addGrade(c, me, 'A')
	c = DA.addCourse('52540', 'CS 373', 'Software Engineering', 'FALL', '2010', 'Glenn Downing')
	DA.addRating(c, me, '100', 'Essential.')
	DA.addGrade(c, me, 'B')
	c = DA.addCourse('55480', 'M 346', 'Applied Linear Algebra', 'FALL', '2010', 'Rodriguez Villegas')
	DA.addRating(c, me, '80', 'Tough class to get a hang of. It really helps if you remember your M 340L material')
	DA.addGrade(c, me, 'B')
	c = DA.addCourse('52435', 'CS 336', 'Analysis of Programs', 'FALL', '2010', 'Margaret Myers')
	DA.addRating(c, me, '90', 'Lecturer is a bit crazy')
	DA.addGrade(c, me, 'B')

	b = DA.addBook("Desperation", "978-0451188465", "Stephen King")
	DA.addRating(b, me, '100', 'Definitely a rainy night page turner');
	i = DA.addInternship('Center for Teaching and Learning', 'Univ. of Texas', 'SPRING', '2010')
	DA.addRating(i, me, '100', 'Great if you\'re preparing yourself for a career in web development');
	p = DA.addPlaceStudy('ENS Basement', 'FALL', '2010')
	DA.addRating(p, me, '100', 'Quiet... Full of geeks!');
	p = DA.addPlaceLive('Ballpark Apartments', 'FALL', '2009')
	DA.addRating(p, me, '90', 'Great if you\'ve got great roommates');
	p = DA.addPlaceEat('Big Bite', 'SPRING', '2010')
	DA.addRating(p, me, '95', 'ZOMG!');
	p = DA.addPlaceFun('Rain', 'SPRING', '2010')
	DA.addRating(p, me, '95', 'Bring yo dolla bills');
	g = DA.addGame('Atari', 'Tetris')
	DA.addRating(p, me, '100')
	g = DA.addGame( 'Nintento Wii', 'Super Smash Brothers: Brawl')
	DA.addRating(p, me, '90', 'A great game to loosen you up after a long day of classes.')

def mrw(DA):
	sid = sidgen()
	pwd = passgen()
	me = DA.addStudent(sid,pwd)
	
	p = DA.addPlaceStudy('ENS Basement', 'FALL', '2010')
	DA.addRating(p, me, '80', 'Used to be quiet until more CS people came here; lots of help around though.')
	g = DA.addGame('iPhone', 'Angry Birds')
	DA.addRating(g, me, '100', 'Awesome physics game.')
	c = DA.addCourse('39105', 'HIS 315L', 'United States Since 1865', 'FALL', '2010', 'H. W. Brands')
	DA.addRating(c, me, '90', 'Cool course; lecturing is really great but he gets off topic.')


main()
