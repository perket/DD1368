__author__ = 'pierrerudin'
from inputs import *
from new_contract import choose_driver

def buyer_login(email,package):
    conn = sqlConnect()
    cur = conn.cursor()

    cur.execute("select bd.id,bd.email,true from buyer_details bd,contracts c where c.buyer = bd.id and bd.email = '%s' and c.id = '%s'" % (email,package))
    cr = cur.rowcount
    if cur.rowcount == 1:
        id,email,buyer = cur.fetchone()
        current_user.login(id,email,False,buyer,package)

    conn.close()

    return cr == 1


def pay():
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("update transactions set paid_by_buyer = now() where contract = '%s'" % current_user.get_order_id())
    conn.commit()
    cur.close()


def get_credit_card_information():
    print("Insert your credit card information without spaces or (0) to go back:")
    _,cont = input_controller("",r"^[0-9]{16}$")
    if cont:
        _,cont = input_controller("Expiration date mm/yy",r"^[0-9]{2}\/[0-9]{2}$")
    if cont:
        _,cont = input_controller("Card security code",r"^[0-9]{3}$")
    return cont


def get_order_status(order_id):
    #STATUSES
    #0 - Order registered
    #1 - Signed by seller
    #2 - Buyer choosed delivery
    #3 - Taken by driver
    #4 - Paid by buyer
    #5 - Package picked-up
    #6 - Packaged delivered
    #7 - Confirmed by buyer
    #8 - Transaction settled
    status = 0
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("select sum(steps_taken) from (select (c.registered is not null) + (c.signed is not null) + (c.buyer_satisfied is not null) + (p.taken_by_driver is not null) + (p.driver is not null) + (p.picked_up is not null) + (p.delivered is not null) as steps_taken from contracts c,packages p where c.package = p.id and c.id = '%s' union select (paid_by_buyer is not null) + (settled is not null) as steps_takens from transactions where contract = '%s') as k;" % (order_id,order_id))
    if cur.rowcount > 0:
        status = cur.fetchone()[0] - 1
    conn.close()
    return status


def delivery_options(driver):
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("select p.width*p.height*p.length/power(10,9) from packages p,contracts c where c.id = '%s' and c.package = p.id" % current_user.get_order_id())
    volume = cur.fetchone()[0]

    cur.execute("call update_driver(%s,%s,'%s')" % (driver,volume,current_user.get_order_id()))
    conn.commit()
    conn.close()

def confirm():
    status = get_order_status(current_user.get_order_id())
    if status == 6:
        print("Have you received your product (y/n)?")
        inp = menu_input(["y","n"])
        if inp == "y":
            print("Are you satisfied with your purchase (y/n)?")
            inp = menu_input(["y","n"])
            if inp == "y":
                conn = sqlConnect()
                cur = conn.cursor()
                cur.execute("update contracts set buyer_satisfied = now() where id = '%s'" % current_user.get_order_id())
                cur.execute("update transactions set settled = now() where contract = '%s'" % current_user.get_order_id())
                conn.commit()
                conn.close()
                print("We are glad that you are satisfied with your purchase and hope you'll continue to use D2D.se in the future.")
            else:
                print("We are sad to hear that you're not satisfied with you're purchase, we will contact the seller for you and try to settle this as quick as possible.")
        else:
            print("We will contact the driver and return to you as soon as we know anything about your package")
    elif status > 6:
        print("You have already confirmed this order.")
    else:
        print("You have to wait until our driver have delivered your package before you can make this step.")


def buyers_menu():
    print_order_details()
    print("""
(1) Delivering options
(2) Pay
(3) Confirm delivery and satisfaction
(0) Log out
""")
    inp = menu_input(["1","2","3","0"])
    if inp == "1":
        delivery_options()
    elif inp == "2":
        pay()
        buyers_menu()
    elif inp == "3":
        confirm()
        buyers_menu()
    elif inp == "4":
        buyers_menu()
    elif inp == "0":
        current_user.logout()
        print("You are now logged out.")


def print_order_details():
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("select c.id,ud.fname,ud.lname,ud.address,ud.zip_code,ud.city,p.width,p.height,p.length,p.weight,c.price,p.content_description,bd.fname,bd.lname,bd.address,bd.zip_code,bd.city from contracts c, packages p, buyer_details bd, user_details ud where c.id = '%s' and c.package = p.id and c.seller = ud.id and c.buyer = bd.id;" % current_user.get_order_id())
    contract_details = cur.fetchone()
    print("""----------------------------------------------------------
                    order id: %s
----------------------------------------------------------
Seller:
%s %s
%s
%s %s
----------------------------------------------------------
Package:
(WxHxL): %sx%sx%s mm
weight: %s g
price: %s SEK
description:
%s
----------------------------------------------------------
Buyer:
%s %s
%s
%s %s
----------------------------------------------------------""" % contract_details)
    cur.close()


