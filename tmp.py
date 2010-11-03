from dataStore import *
import random
import dataAccessors

x = Ratable.all().get()

print x.__class__.__name__

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
def uidgen():
    return randString(8)
def passgen():
    return randString(12)

DA = dataAccessors.DataAccessor()
uid = uidgen()
pw = passgen()
DA.addAdmin(uid, pw)



print uid
print pw
