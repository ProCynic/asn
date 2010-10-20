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
    pat
    if re.search("^\d{5}$",value) is None: raise ValueError


def courseNumValidator(value):
    """
    """
    pattern = "^[A-Z]{1,3}\s\d{3}[a-zA-Z]?$"
    if re.search(pattern,value) is None: raise ValueError


def personNameValidator(value):
    """
    """
    pattern = "^.*$"
    if re.search(pattern,value) is None: raise ValueError

def gradeValidator(value):
    """
    """
    pattern = "^([B-D][\+|\-]?)|A\-?|F$"
    if re.search(pattern,value) is None: raise ValueError

def yearValidator(value):
    """
    """
    pattern = "^\d{4}$"
    if re.search(pattern,value) is None: raise ValueError
