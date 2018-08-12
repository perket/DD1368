from new_member import *
from new_contract import *
from buyer import *
from driver import *

def start_screen():
    print("Welcome to D2D.se - your number one payment/delivery provider.")


def login(driver,email,pWord):
    # email,cont = input_controller("E-mail",r"[^@]+@[^@]+\.[^@]+")
    # if cont:
    #     password,cont = password_input()
    # if cont:
    password = hash(pWord)
    print(driver,email,password)
    conn = sqlConnect()
    cur = conn.cursor()
    if not driver:
        cur.execute("select id,email,false from user_details where email = '%s' and password = '%s'" % (email,password))
    else:
        cur.execute("select dd.id,ud.email,true from user_details ud,driver_details dd where ud.id = dd.id and ud.email = '%s' and ud.password = '%s'" % (email,password))
    rc = cur.rowcount

    if rc == 1:
        id,email,drvr = cur.fetchone()
        current_user.login(id,email,drvr,False,None)
    conn.close()
    return rc == 1


def sellers_menu():
    print("""(1) Set up contract
(0) Log out
""")
    inp = menu_input(["1","2","3","0"])
    if inp == "1":
        new_contract()
    elif inp == "0":
        current_user.logout()
        print("You are now logged out.")


def head_menu():
    if not current_user.is_active():
        print("""(1) Member login
(2) Driver login
(3) Buyer login
(4) New member
(0) Quit
""")

        inp = menu_input(["1","2","3","4","0"])
        if inp == "1":
            login(False)
            head_menu()
        if inp == "2":
            login(True)
            head_menu()
        if inp == "3":
            buyer_login()
            head_menu()
        elif inp == "4":
            register_new_user()
            head_menu()
        elif inp == "0":
            print("Thank you for using D2D.se, we hope to see you soon again!")

    else:
        if current_user.is_driver():
            drivers_menu()
        elif current_user.is_buyer():
            buyers_menu()
        else:
            sellers_menu()
        head_menu()


#start_screen()
#head_menu()