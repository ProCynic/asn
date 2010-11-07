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

def getUserGrade(course, user) :
    if not user :
        return None

    query = DS.Grade.all()
    query.filter('student =', user)
    query.filter('course =', course)

    if (query.count() == 1) :
        grade = query.get()
        return grade.grade
    else :
        return None


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

def prepareItem(x, user = None) :
    u = unify(x)

    u.rating, u.ratingCount = getAverageRating(x)
    u.ratingClass = getRatingClass(u.rating)
    u.dbkey = str(x.key())

    if (isinstance(x, DS.Course)) :
        u.avgGrade = getAverageGrade(x)
        
        userGrade = getUserGrade(x, user)
        if userGrade:
            u.studentGrade = userGrade
        else :
            u.studentGrade = None
    else :
       u.avgGrade = None

    return u


def prepareDataForTemplate(query) :
    temp = []
    for x in query :
        u = prepareItem(x)

        temp.append(u)
    return temp

def prepareRatingsForTemplate(query, user) :
    temp = []
    for x in query :
        u = prepareItem(x.rated, user)
        u.studentRating = x.rating

        if (x.comment) :
            u.studentComment = x.comment.text
        else :
            u.studentComment = "No Comment"
        
        temp.append(u)

    return temp

#Transforms any Ratable object into a standard interface.
#This consists of only data directly from the data store.
#For calculated data, such as average rating, average grade, and the dbkey
# invoke prepareDataForTemplate on a collection of ratables instead.

class DetailEntry :
    prefix = None
    data = None


class UnifiedRatable :
    def __init__(self) :
        #A user-displayable type for the ratable object.
        self.type = None

        #A generic name for the ratable.
        #For example, for books, this will be their title.
        self.name = None
        self.details = []

        #This is set if we were flattened from the ratings 
        self.studentRating = None
        self.studentComment = None
        self.studentGrade = None
    
    def addDetail(self, prefix, data) :
        d = DetailEntry()
        d.prefix = prefix
        d.data = data
        self.details.append(d)

        self.i = len(self.details)

def unify(i) :
    result = UnifiedRatable()

    if isinstance(i, DS.Course) :
        result.type = "Course"
        result.name = "%s : %s (%s)" % (i.courseNum, i.name, i.unique)

        result.addDetail("Instructor:", str(i.instructor))
        result.addDetail("Semester:", "%s, %s" % (i.semester.capitalize(), i.year))
    
    elif isinstance(i, DS.Book) :
        result.type = "Book"
        result.name = "%s" % (i.title)
        
        result.addDetail("Author:", i.author)
        result.addDetail("ISBN:", i.isbn)

    elif isinstance(i, DS.Paper) :
        result.type = i.paperType.capitalize()
        result.name = "%s" % (i.title)

        result.addDetail("Author:", str(i.author))

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
    
        result.addDetail("At", str(i.location))
        result.addDetail("Semester:", "%s, %s" % (i.semester.capitalize(), i.year))

    elif isinstance(i, DS.Game) :
        result.name = i.title 
        result.addDetail("Platform:", i.platform)

    return result
