from dataAccessors import *

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
    

def main():
    gparker()
    aywang()
    ttb265()
    matt()



def gparker():
    sid = sidgen()
    pwd = passgen()
    me = addStudent(sid,pwd)

    b = addBook("The Good Fairies of New York", "978-0765358547", "Martin Millar")
    addRating(b, me, '100', "Excellent British humor by a lesser know author")
    


def aywang():
    sid = sidgen()
    pwd = passgen()
    me = addStudent(sid,pwd)

def ttb265():
    sid = sidgen()
    pwd = passgen()
    me = addStudent(sid,pwd)

def matt():
    sid = sidgen()
    pwd = passgen()
    me = addStudent(sid,pwd)
