from new_member import *
from new_contract import *
from buyer import *
from driver import *

def login(driver,email,pWord):
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
