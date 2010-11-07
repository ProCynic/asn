import dataStore as DS
from dataAccessors import * 

def getAverageRating(item) :
    query = DS.Rating.all()
    query.filter('rated =', item)

    items = 0
    total = 0
    for x in query : 
        total += x.rating
        items += 1

    if items == 0 :
        return (0, 0)

    return (total / items, items);


def getRatingClass(rating) :
    if rating > 70 :
        return 'good' 
    
    if 70 >= rating and rating > 40 :
        return 'average'

    return 'bad'

def getAverageGrade(item) :
    query = DS.Grade.all()
    query.filter('course =', item)

    grademap = { 
        'A' : 4.0, 
        'A-' : 3.67,
        'B+' : 3.33,
        'B' : 3.0,
        'B-' : 2.67,
        'C+' : 2.33,
        'C' : 2.0,
        'C-' : 1.67,
        'D+' : 1.33,
        'D' : 1,
        'D-' :0.67,
        'F' : 0
    }
    
    #This is a map of gpa -> letter
    valuemap = dict([ (v, k) for (k, v) in grademap.iteritems()])

    #Accumulate the grades, translated into GPA points.
    grade = 0
    count = 0
    for x in query : 
        g = x.grade.upper()
        if g in grademap :
            grade += grademap[g]
            count += 1

    if count == 0 :
        return 'None'

    #Average the GPA and then find the letter that should be assigned to it.
    grade = grade / count

    prevgrade = 0
    for x in sorted(grademap.values()) :
        #Once we find a letter higher than our grade, return the previous letter.
        if (grade < x) :
            grade = prevgrade
            break
        prevgrade = x
            
    return valuemap[grade];

def prepareDataForTemplate(query) :
    query = addTypename(query)
    temp = []
    for x in query :

        u = unify(x)

        u.rating, u.ratingCount = getAverageRating(x)
        u.ratingClass = getRatingClass(u.rating)
        u.dbkey = str(x.key())

        if (isinstance(x, DS.Course)) :
            u.avgGrade = getAverageGrade(x)
        else :
            u.avgGrade = None

        temp.append(u)
    return temp


#Transforms any Ratable object into a standard interface.
#This consists of only data directly from the data store.
#For calculated data, such as average rating, average grade, and the dbkey
# invoke prepareDataForTemplate on a collection of ratables instead.
class UnifiedRatable : 
    
    #A user-displayable type for the ratable object.
    type = None

    #A generic name for the ratable.
    #As an example, for books, this will be their title.
    name = None

    #A number of optional parameters follow.

    #The semester and year that the ratable applies to. 
    #Does not exist for books, papers anid games.
    semester = None

    #The instructor's name. Exists only for courses.
    instructor = None

    #The author of a book / paper.
    author = None

    #The ISBN of a book
    isbn = None

    #The platform for a game.
    platform = None


def unify(i) :
    result = UnifiedRatable()

    if isinstance(i, DS.Course) :
        result.type = "Course"
        result.name = "%s : %s (%s)" % (i.courseNum, i.name, i.unique)
        result.semester = "%s, %s" % (i.semester.capitalize(), i.year)
        result.instructor = str(i.instructor)
    
    elif isinstance(i, DS.Book) :
        result.type = "Book"
        result.name = "%s" % (i.title)
        result.author = str(i.author)
        result.isbn = i.isbn

    elif isinstance(i, DS.Paper) :
        result.type = i.paperType.capitalize()
        result.name = "%s" % (i.title)
        result.author = str(i.author)

    elif isinstance(i, DS.Place) :
        placeTypeMapping = {
            "Internship" : "Internship",
            "PlaceLive" : "Living Place", 
            "PlaceEat" : "Eating Place",
            "PlaceFun" : "Fun Place",
            "PlaceStudy" : "Studing Place",
        }

        result.type = placeTypeMapping[getUndecoratedTypename(i)]
        result.name = i.name
        result.semester = "%s, %s" % (i.semester.capitalize(), i.year)
        result.location = str(i.location)

    elif isinstance(i, DS.Game) :
        result.name = i.title 
        result.platform = i.platform

    return result
