"""
"""
import re

def uniqueValidator(value):
    """
    """
    unique = re.search("^\d{5}$",value)
    if unique is None: raise ValueError
