import dataStore as DS
from dataAccessors import addTypename

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
        x.rating, x.ratingCount = getAverageRating(x)
        x.ratingClass = getRatingClass(x.rating)
        x.dbkey = str(x.key())

        if (isinstance(x, DS.Course)) :
            x.avgGrade = getAverageGrade(x)

        temp.append(x)
    return temp
