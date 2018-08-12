__author__ = 'pierrerudin'
import pymysql
from hashlib import sha1
from getpass import getpass
import re

class User():
    def __init__(self):
        self.user_id = None
        self.user_name = None
        self.driver = False
        self.buyer = False
        self.active = False
        self.order = None

    def login(self,user_id,username,driver,buyer,order):
        self.user_id = user_id
        self.user_name = username
        self.driver = driver
        self.buyer = buyer
        self.active = True
        self.order = order

    def logout(self):
        self.user_id = None
        self.user_name = None
        self.driver = False
        self.buyer = False
        self.active = False
        self.order = None

    def get_id(self):
        return self.user_id

    def is_active(self):
        return self.active

    def is_driver(self):
        return self.driver

    def is_buyer(self):
        return self.buyer

    def get_order_id(self):
        return self.order

current_user = User()

def sqlConnect():
    return pymysql.connect(host='HOST',port=3306,user='USER',passwd='PASSWORD',db='DATABASE')


