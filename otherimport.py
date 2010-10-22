class dataHolder:
    pass

for student in f.getroot():
    assert student.tag == 'student'
    ids = student.getNodes('id')
    assert len(ids) == 1
    sid = ids[0]
    for elem in student:
        if elem.tag == 'id': pass
        elif elem.tag == 'class': parseClass(elem)
        elif elem.tag == 'internship': parseInternship(elem)
        elif elem.tag == 'book': parseBook(elem)
        ...
        else: raise ValueError

def parse(elem):
    data = {}
    for item in elem:
        data[argnames[item.tag]] = item.text.strip()
    
