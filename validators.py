"""
"""
import re

#Template
def Validator(value):
    """
    """
    pattern = "^$"
    if re.search(pattern,value) is None: raise ValueError

def uniqueValidator(value):
    """
    """
    pattern = "^\d{5}$"
    if re.search(pattern,value) is None: raise ValueError


def courseNumValidator(value):
    """
    """
    pattern = "^[A-Z]{1,3}\s\d{3}[a-zA-Z]?$"
    if re.search(pattern,value) is None: raise ValueError


def gradeValidator(value):
    """
    """
    #pattern = "^([B-D][\+|\-]?)|(A\-?)|F$"
    #if re.search(pattern,value) is None: raise ValueError
    if value not in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F'] : raise ValueError
def yearValidator(value):
    """
    """
    pattern = "^\d{4}$"
    if re.search(pattern,value) is None: raise ValueError

def isbnValidator(value):
    """
    """
    pattern = "^\d{10}|\d{13}$"
    if re.search(pattern,value) is None: raise ValueError
    x = [int(i) for i in value[:-1]]
    s = int(value[-1])
    #For ISBN-10
    if len(value) == 10:
        if s != 11 - sum(x[i]*(10-i) for i in range(len(x))) % 11: raise ValueError
    #For ISBN-13
    for i in range(1,len(x)+1,2):
        x[i] *= 3
    if s != 10 - (sum(x) % 10): raise ValueError
