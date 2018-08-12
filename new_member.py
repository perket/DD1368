__author__ = 'pierrerudin'
from inputs import *

def save_user_data(fname, lname, email, password, address, zip_code, city, bank_routing_num, bank_account_num, driver):
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("call register_user('%s','%s','%s','%s','%s',%s,'%s',%s,%s,%s)" % (fname, lname, email, password, address, zip_code, city, bank_routing_num, bank_account_num,driver))
    conn.commit()
    conn.close()


def register_new_user():
    pass
def register_new_user(member_type,fName,lName,email,pWord,address,zip,city,brn,ban):
    print("""Finish the following form to register as member at D2D.se.
You may only use characters a-z,A-Z and 0-9 in your password which must be at least 6 characters long.
The address you provide during registration will serve as pick-up address.
You can return to head menu at any time by leaving a single 0 as answer to any of the given qustions.""")

    print("""What kind of membership do you wish to register?
(1) Regular
(2) Driver
(0) Go back""")
    member_type = menu_input(["1","2","0"])
    cont = True
    if member_type == "0":
        cont = False

    if cont:
        fname,cont = input_controller("First name",r"^[a-zA-ZåäöÅÄÖ ]*$")
    if cont:
        lname,cont = input_controller("Last name",r"^[a-zA-ZåäöÅÄÖ ]*$")
    if cont:
        email,cont = email_input()
    if cont:
        password,cont = password_input()
    if cont:
        address,cont = input_controller("Address",r"^[a-zA-Z0-9åäöÅÄÖ ]*$")
    if cont:
        zip_code,cont = input_controller("Zip code",r"^[0-9]{5}$")
    if cont:
        city,cont = input_controller("City",r"^[a-zA-ZåäöÅÄÖ ]*$")
    if cont:
        bank_routing_num,cont = input_controller("Bank routing number",r"^([0-9]{4}|[0-9]{5})$")
    if cont:
        bank_account_num,cont = input_controller("Bank account number",r"^([0-9]{7}|[0-9]{9}|[0-9]{10})$")

    if cont:
        print("""----------------------------------------------------------
                         User data
----------------------------------------------------------
Name: %s %s
E-mail: %s
Address: %s
Zip code: %s
City: %s
Bank details: %s %s
----------------------------------------------------------
""" % (fname,lname,email,address,zip_code,city,bank_routing_num,bank_account_num))
        save_user_data(fname,lname,email,password,address,int(zip_code),city,int(bank_routing_num),int(bank_account_num),member_type=="2")