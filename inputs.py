__author__ = 'pierrerudin'
from init import *

def menu_input(good_inputs):
    good_input = False
    while not good_input:
        inp = input()
        if inp in good_inputs:
            good_input = True
        else:
            print("Bad input!")
    return inp


def input_controller(title,reg):
    good_input = False
    while not good_input:
        inp = input(title+": ")
        if re.match(reg, inp) or inp == "0":
            good_input = True
        else:
            print("Bad input, try again.")
    return inp,inp is not "0"


def email_input():
    conn = sqlConnect()
    cur = conn.cursor()
    good_input = False
    while not good_input:
        inp = input("E-mail: ")
        if re.match(r"[^@]+@[^@]+\.[^@]+", inp) or inp == "0":
            cur.execute("Select * from user_details where email = '%s'" % inp)
            if cur.rowcount == 0:
                good_input = True
            else:
                print("E-mail address is allready registered!")
        else:
            print("Bad input, try again.")
    conn.close()
    return inp,inp is not "0"


def password_input():
    good_pass = False
    while not good_pass:
        inp = getpass()
        if (re.match(r"^[a-zA-Z0-9_]*$", inp) and len(inp) >= 6) or inp == "0":
            good_pass = True
        else:
            print("Bad input, try again!")
    h = sha1()
    h.update(inp.encode("utf-8"))
    return h.hexdigest(),inp is not "0"

def hash(inp):
    h = sha1()
    h.update(inp.encode("utf-8"))
    return h.hexdigest()