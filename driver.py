__author__ = 'pierrerudin'
from inputs import *

def list_packages(query):
    inputs = ["0"]
    packages = []
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute(query)
    if cur.rowcount > 0:
        print("#".ljust(6)+"delivery address".ljust(65)+"pick-up address\n------------------------------------------------------------------------------------------------------------------------------------------------------")
        i = 1
        for pId,bFname,bLname,bAddress,bZip,bCity,sFname,sLname,sAddress,sZip,sCity in cur:
            print("("+str(i).ljust(2)+")  "+(bFname+" "+bLname+", "+bAddress+", "+" "+bCity).ljust(65)+sFname+" "+sLname+", "+sAddress+", "+sZip+" "+sCity)
            inputs.append(str(i))
            packages.append(pId)
            i += 1
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
    conn.close()
    return inputs,packages


def accpet_delivery():

    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("select p.id from packages p,contracts c where c.package = p.id and c.id = '%s'" % current_user.get_order_id())
    package = cur.fetchone()[0]
    cur.execute("call take_package(%s)" % package)
    conn.commit()
    conn.close()


def register_pickup():
    query = "select p.id,bd.fname,bd.lname,bd.address,bd.zip_code,bd.city,ud.fname,ud.lname,ud.address,ud.zip_code,ud.city from packages p,contracts c,user_details ud,buyer_details bd,transactions t where p.id = c.package and c.buyer = bd.id and c.seller = ud.id and p.driver = %s and t.contract = c.id and t.paid_by_buyer is not null and p.picked_up is null" % current_user.get_id()
    inputs,packages = list_packages(query)
    if len(packages) > 0:
        print("Select package to pick-up or (0) to go back:")
        inp = menu_input(inputs)
        if inp != "0":
            package = packages[int(inp) - 1]
            conn = sqlConnect()
            cur = conn.cursor()
            cur.execute("update packages set picked_up = now() where id = '%s'" % package)
            conn.commit()
            conn.close()
            register_pickup()
    else:
        print("You have no packages to pick-up.")


def register_delivery():
    query = "select p.id,bd.fname,bd.lname,bd.address,bd.zip_code,bd.city,ud.fname,ud.lname,ud.address,ud.zip_code,ud.city from packages p,contracts c,user_details ud,buyer_details bd,transactions t where p.id = c.package and c.buyer = bd.id and c.seller = ud.id and p.driver = %s and t.contract = c.id and t.paid_by_buyer is not null and p.picked_up is not null and p.delivered is null" % current_user.get_id()
    inputs,packages = list_packages(query)
    if len(packages) > 0:
        print("Select package to deliver or (0) to go back:")
        inp = menu_input(inputs)
        if inp != "0":
            package = packages[int(inp) - 1]
            conn = sqlConnect()
            cur = conn.cursor()
            cur.execute("update packages set delivered = now() where id = '%s'" % package)
            conn.commit()
            conn.close()
            register_delivery()
    else:
        print("You have no packages to deliver!")


def drivers_menu():
    print("""(1) Edit pricing and estimated shipment time
(2) Accept possible shipments
(3) Register pick-up
(4) Register delivery
(0) Log out
""")
    inp = menu_input(["1","2","3","4","0"])
    if inp == "1":
        adjust_price()
        drivers_menu()
    elif inp == "2":
        accpet_delivery()
        drivers_menu()
    elif inp == "3":
        register_pickup()
        drivers_menu()
    elif inp == "4":
        register_delivery()
        drivers_menu()
    elif inp == "0":
        current_user.logout()
        print("You are now logged out.")


def adjust_price():
    print("""Enter a new price per delivered cubic meter and estimated delivery time in days, the currency that's used is SEK.
To leave the fields unchanged simply enter 0.""")
    new_price,adjust_p = input_controller("Price",r"^[0-9]*$")
    new_delivery_time,adjust_dt = input_controller("Shipping time in days",r"^[0-9]*$")
    if adjust_p or adjust_dt:
        conn = sqlConnect()
        cur = conn.cursor()
        update_p = update_dt = comma = ""
        if adjust_p:
            update_p = "price = %s" % int(new_price)
        if adjust_dt:
            update_dt = "delivery_time = %s" % int(new_delivery_time)
        if adjust_dt and adjust_p:
            comma = ","
        cur.execute("Update driver_details set %s%s %s where id = %s" % (update_p,comma,update_dt,current_user.get_id()))
        conn.commit()
        conn.close()
        print("Updates completed!")