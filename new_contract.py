__author__ = 'pierrerudin'
from inputs import *
import string
import random

def list_drivers(volume):
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("select dd.id,concat(ud.fname,' ',ud.lname),dd.price,dd.delivery_time from driver_details dd,user_details ud where dd.id = ud.id")
    drivers = []
    inputs = ["0"]
    i = 0
    for drvr_id,name,price,delivery_time in cur:
        print("("+str(i+1)+")".ljust(3)+str(name).ljust(25)+(str(int(price*volume+.5))+" SEK").rjust(12)+str(delivery_time).rjust(len(str(delivery_time))+2)+" days to deliver")
        drivers.append(drvr_id)
        inputs.append(str(i+1))

        i += 1
    conn.close()
    return drivers,inputs


def choose_driver(volume):
    drivers,inputs = list_drivers(volume)
    inp = menu_input(inputs)
    if inp != "0":
        return drivers[int(inp)-1],True
    else:
        return 0,False


def save_contract(contract_id,buyer_id,price,content,width,height,length,weight):
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("call register_contract('%s',%s,%s,%s,'%s',%s,%s,%s,%s)" % (contract_id,buyer_id,current_user.get_id(),price,content,width,height,length,weight))
    conn.commit()
    conn.close()

def save_buyer(fname,lname,email,address,zip_code,city):
    print("insert into buyer_details (fname,lname,email,address,zip_code,city) values ('%s','%s','%s','%s',%s,'%s')" % (fname,lname,email,address,zip_code,city))
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("select id from buyer_details where email = '%s'" % email)
    if cur.rowcount == 0:
        cur.execute("insert into buyer_details (fname,lname,email,address,zip_code,city) values ('%s','%s','%s','%s','%s','%s')" % (fname,lname,email,address,zip_code,city)) # insert into
        conn.commit()
        cur.execute("select id from buyer_details where email = '%s'" % email)
        id = cur.fetchone()[0]
    else:
        id = cur.fetchone()

    conn.close()
    return id


def generate_contract_id():
    conn = sqlConnect()
    cur = conn.cursor()
    bad = True
    while bad:
        gen_id = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(6))
        cur.execute("select * from contracts where id = '%s'" % gen_id)
        if cur.rowcount == 0:
            bad = False
    return gen_id


def get_contract_data(contract_id):
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("""select
    bd.fname, bd.lname, bd.email, bd.address, bd.zip_code, bd.city, p.content_description, c.price, p.width, p.length, p.height, p.weight
    from contracts c,packages p,buyer_details bd where c.id = '%s' and c.package = p.id and bd.id = c.buyer""" % contract_id)
    buyer_fname,buyer_lname,email,address,zip,city,content,price,width,height,length,weight = cur.fetchone()
    conn.close()
    return buyer_fname,buyer_lname,email,address,zip,city,content,price,width,height,length,weight


def get_signature():
    print("To sign, enter your password: ")
    pword,_ = password_input()
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("select true from user_details where id = %s and password = '%s'" % (current_user.get_id(),pword))
    correct_pword = cur.fetchone()[0]
    conn.close()
    if correct_pword:
        return True
    else:
        print("Wrong password!")
        return get_signature()


def delete_contract(contract_id):
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("call drop_contract('%s')" % contract_id)

    conn.commit()
    conn.close()


def sign_contract(contract_id):
    buyer_fname,buyer_lname,email,address,zip,city,content,price,width,height,length,weight = get_contract_data(contract_id)
    print("""To validate the contract we now need you to sign it.

----------------------------------------------------------
                        Contract (%s)
----------------------------------------------------------
Buyer: %s %s
E-mail: %s
Address: %s
Zip code: %s
City: %s

Content: %s
Price: %s SEK
Volume: %s m3
Weight: %s g
----------------------------------------------------------

Is this correct? (y/n)
""" % (contract_id,buyer_fname,buyer_lname,email,address,zip,city,content,price,(int(width)*int(height)*int(length))/10**9,weight))
    inp = menu_input(["y","n"])
    if inp == "y":
        if get_signature():
            print("Contract signed!\nWe will now inform the buyer.")
            return True
        return False
    else:
        print("Since there is something wrong with the contract you've set up, we will now remove it and you may try again.")
    return False


def save_signed_contract(contract_id):
    conn = sqlConnect()
    cur = conn.cursor()
    cur.execute("update contracts set signed = now() where id = '%s'" % contract_id)

    conn.commit()
    conn.close()
    pass


def new_contract():
    print("Provide information about the buyer, (0) to go back:")

    fname,cont = input_controller("First name",r"^[a-zA-ZåäöÅÄÖ ]*$")
    if cont:
        lname,cont = input_controller("Last name",r"^[a-zA-ZåäöÅÄÖ ]*$")
    if cont:
        email,cont = input_controller("E-mail",r"[^@]+@[^@]+\.[^@]+")
    if cont:
        address,cont = input_controller("Address",r"^[a-zA-Z0-9åäöÅÄÖ ]*$")
    if cont:
        zip_code,cont = input_controller("Zip code",r"^[0-9]{5}$")
    if cont:
        city,cont = input_controller("City",r"^[a-zA-ZåäöÅÄÖ ]*$")

    buyer_id,cont = save_buyer(fname,lname,email,address,zip_code,city,cont)

    if cont:
        print("Provide information about the item being sold including packaging information:, (0) to go back")
        price,cont = input_controller("Price",r"^[0-9]*$")
    if cont:
        width,cont = input_controller("Width [mm]",r"^[0-9]*$")
    if cont:
        height,cont = input_controller("Height [mm]",r"^[0-9]*$")
    if cont:
        length,cont = input_controller("length [mm]",r"^[0-9]*$")
    if cont:
        weight,cont = input_controller("weight [g]",r"^[0-9]*$")
    if cont:
        content,cont = input_controller("Content description",r"")
    #if cont:
    #    driver,cont = choose_driver((int(width)*int(height)*int(length))/10**9)
    if cont:
        contract_id = generate_contract_id()
        save_contract(contract_id,buyer_id,price,content,int(width),int(height),int(length),int(weight))
        
        signed = sign_contract(contract_id)
        if signed:
            save_signed_contract(contract_id)
        else:
            delete_contract(contract_id)
