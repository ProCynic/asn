addBook(title,isbn,author):
    isbn = isbn.strip().replace('-','')
    #pull out fname, lname, mname from author

    a = addPerson(afname,alname,amname)
    b = Book(title=title,
             isbn=isbn,
             author=a)

def addPerson(fname,lname, mname=None):
    #if person in datastore:
        #return person.key()
    p = Person(fname=fname,
               lname=lname,
               mname=mname)
    p.put()
    return p.key()

def addCourse(unique, courseNum, name, semester, instructor, grade):
    #regexps to pull out data
    
