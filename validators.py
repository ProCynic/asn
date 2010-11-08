"""
"""
import re

#Template
def Validator(value):
    """
    Validator Template.  Never actually used.
    """
    pattern = "^$"
    if re.search(pattern,value) is None: raise ValueError

def uniqueValidator(value):
    """
    Validates a course unique number.
    5 digits
    """
    pattern = "^\d{5}$"
    if re.search(pattern,value) is None: raise ValueError


def courseNumValidator(value):
    """
    Validates a course num.
    1-3 chars, then whitespace, then 3 digits, then optional char
    Eg. "CS 373" or "M 358K"
    """
    pattern = "^[A-Z]{1,3}\s\d{3}[a-zA-Z]?$"
    if re.search(pattern,value) is None: raise ValueError


def gradeValidator(value):
    """
    Validates a grade.
    A-F with +- on B-D and A-
    """
    #pattern = "^([B-D][\+|\-]?)|(A\-?)|F$"
    #if re.search(pattern,value) is None: raise ValueError
    if value not in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'] : raise ValueError
def yearValidator(value):
    """
    Validates a year.
    4 digits
    """
    pattern = "^\d{4}$"
    if re.search(pattern,value) is None: raise ValueError

def isbnValidator(value):
    """
    Validates a book ISBN
    Uses actual ISBN 10 or 13 checksum calculator.
    """
    if len(value) != 10 and len(value) != 13 : raise ValueError
    x = [int(i) for i in value[:-1]]
    s = int(value[-1])
    #For ISBN-10
    if len(value) == 10:
        if s != 11 - sum(x[i]*(10-i) for i in range(len(x))) % 11: raise ValueError
    #For ISBN-13
    elif len(value) == 13:
    	for i in range(1,len(x)+1,2):
        	x[i] *= 3
    	if s != 10 - (sum(x) % 10): raise ValueError

def studentValidator(value):
    """
    Validates that the user given is a student.
    """
    if value.userType != 'STUDENT': raise ValueError
