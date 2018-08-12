__author__ = 'pierrerudin'

import tkinter as tk
from new_member import *
from new_contract import *
from buyer import *
from driver import *
from d2d import *

class GUI(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container = tk.Frame(self)

        container.grid()

        self.frames = {}

        for F in (StartMenu,UserLogin,DriverLogin,BuyerLogin,NewMember,UserMenu,NewContract,BuyerMenu,PayOrder):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0,column=0,sticky="nsew")

        self.show_frame(StartMenu)

    def show_frame(self,controller):
        frame = self.frames[controller]
        frame.tkraise()



class StartMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        label = tk.Label(self,text="Welcome to D2D.se",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')

        uLogin = tk.Button(self,text="Member login",command= lambda: controller.show_frame(UserLogin))
        uLogin.grid(column=0,row=1)

        dLogin = tk.Button(self,text="Driver login",command=lambda: controller.show_frame(DriverLogin))
        dLogin.grid(column=0,row=2)

        bLogin = tk.Button(self,text="Buyer login",command=lambda: controller.show_frame(BuyerLogin))
        bLogin.grid(column=0,row=3)

        nMember = tk.Button(self,text="New member",command=lambda: controller.show_frame(NewMember))
        nMember.grid(column=0,row=4)


class UserMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.labelText = tk.StringVar()
        label = tk.Label(self,text="User menu",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=1,sticky='EW')

        contract = tk.Button(self,text="New Contract",command=lambda: controller.show_frame(NewContract))
        contract.grid(column=0,row=1)

        logoutButton = tk.Button(self,text="Log out",command=lambda: self.logout())
        logoutButton.grid(column=0,row=2)

    def logout(self):
        current_user.logout()
        self.controller.show_frame(StartMenu)


class NewContract(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Set up contract",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=1,sticky='EW')


        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Buyer details:",fg="black",bg="white")
        label.grid(column=0,row=1,columnspan=1,sticky='EW')

        self.fNameLable = tk.Label(self,text="First name:")
        self.fNameLable.grid(column=0,row=2,sticky='EW')
        self.fName = tk.Entry(self)
        self.fName.grid(column=1,row=2,sticky='EW')

        self.lNameLable = tk.Label(self,text="Last name:")
        self.lNameLable.grid(column=0,row=3,sticky='EW')
        self.lName = tk.Entry(self)
        self.lName.grid(column=1,row=3,sticky='EW')

        self.emailLable = tk.Label(self,text="E-mail:")
        self.emailLable.grid(column=0,row=4,sticky='EW')
        self.email = tk.Entry(self)
        self.email.grid(column=1,row=4,sticky='EW')

        self.addressLable = tk.Label(self,text="Address:")
        self.addressLable.grid(column=0,row=5,sticky='EW')
        self.address = tk.Entry(self)
        self.address.grid(column=1,row=5,sticky='EW')

        self.zipLable = tk.Label(self,text="Zip-code:")
        self.zipLable.grid(column=0,row=6,sticky='EW')
        self.zip = tk.Entry(self)
        self.zip.grid(column=1,row=6,sticky='EW')

        self.cityLable = tk.Label(self,text="City:")
        self.cityLable.grid(column=0,row=7,sticky='EW')
        self.city = tk.Entry(self)
        self.city.grid(column=1,row=7,sticky='EW')


        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Package details:",fg="black",bg="white")
        label.grid(column=0,row=8,columnspan=1,sticky='EW')

        self.contentLable = tk.Label(self,text="Content:")
        self.contentLable.grid(column=0,row=9,sticky='EW')
        self.content = tk.Entry(self)
        self.content.grid(column=1,row=9,sticky='EW')

        self.priceLable = tk.Label(self,text="Price:")
        self.priceLable.grid(column=0,row=10,sticky='EW')
        self.price = tk.Entry(self)
        self.price.grid(column=1,row=10,sticky='EW')

        self.widthLable = tk.Label(self,text="Width:")
        self.widthLable.grid(column=0,row=11,sticky='EW')
        self.width = tk.Entry(self)
        self.width.grid(column=1,row=11,sticky='EW')

        self.heightLable = tk.Label(self,text="Height:")
        self.heightLable.grid(column=0,row=12,sticky='EW')
        self.height = tk.Entry(self)
        self.height.grid(column=1,row=12,sticky='EW')

        self.lengthLable = tk.Label(self,text="Length:")
        self.lengthLable.grid(column=0,row=13,sticky='EW')
        self.length = tk.Entry(self)
        self.length.grid(column=1,row=13,sticky='EW')

        self.weightLable = tk.Label(self,text="Weight:")
        self.weightLable.grid(column=0,row=14,sticky='EW')
        self.weight = tk.Entry(self)
        self.weight.grid(column=1,row=14,sticky='EW')

        rButton = tk.Button(self,text="Register order",command=lambda: self.register_order())
        rButton.grid(column=0,row=15)

        bButton = tk.Button(self,text="Go Back",command=lambda: controller.show_frame(UserMenu))
        bButton.grid(column=1,row=15)

    def register_order(self):
        buyer_id = save_buyer(self.fName.get(),self.lName.get(),self.email.get(),self.address.get(),self.zip.get(),self.city.get())
        contract_id = generate_contract_id()
        save_contract(contract_id,buyer_id,self.price.get(),self.content.get(),int(self.width.get()),int(self.height.get()),int(self.length.get()),int(self.weight.get()))
        self.controller.show_frame(UserMenu)


class UserLogin(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        label = tk.Label(self,text="Member login",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')

        self.uLable = tk.Label(self,text="E-mail:")
        self.uLable.grid(column=0,row=1,columnspan=1,sticky='EW')
        self.uName = tk.Entry(self)
        self.uName.grid(column=1,row=1,sticky='EW')

        self.pLable = tk.Label(self,text="Password:")
        self.pLable.grid(column=0,row=2,columnspan=1,sticky='EW')
        self.pWord = tk.Entry(self,show="*")
        self.pWord.grid(column=1,row=2,sticky='EW')

        login = tk.Button(self,text="Sign in",command=lambda: self.loginCheck())
        login.grid(column=0,row=3)

        bButton = tk.Button(self,text="Go back",command=lambda: controller.show_frame(StartMenu))
        bButton.grid(column=1,row=3)

    def loginCheck(self):
        loggedIn = login(False,self.uName.get(),self.pWord.get())
        if loggedIn:
            self.controller.show_frame(UserMenu)
            #TODO member menu
        else:
            #TODO error message
            print("FAIL")


class DriverLogin(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Driver login",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')

        self.uLable = tk.Label(self,text="E-mail:")
        self.uLable.grid(column=0,row=1,sticky='EW')
        self.uName = tk.Entry(self)
        self.uName.grid(column=1,row=1,sticky='EW')

        self.pLable = tk.Label(self,text="Password:")
        self.pLable.grid(column=0,row=2,sticky='EW')
        self.pWord = tk.Entry(self,show="*")
        self.pWord.grid(column=1,row=2,sticky='EW')

        login = tk.Button(self,text="Sign in",command=lambda: self.loginCheck())
        login.grid(column=0,row=3)

        bButton = tk.Button(self,text="Go back",command=lambda: controller.show_frame(StartMenu))
        bButton.grid(column=1,row=3)

    def loginCheck(self):
        loggedIn = login(True,self.uName.get(),self.pWord.get())
        if loggedIn:
            #TODO driver menu
            print("SUCCESS")
        else:
            #TODO error message
            print("FAIL")





class BuyerLogin(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Buyer login",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')

        self.uLable = tk.Label(self,text="E-mail:")
        self.uLable.grid(column=0,row=1,sticky='EW')
        self.uName = tk.Entry(self)
        self.uName.grid(column=1,row=1,sticky='EW')

        self.cIDLable = tk.Label(self,text="Contract-ID:")
        self.cIDLable.grid(column=0,row=2,sticky='EW')
        self.cID = tk.Entry(self)
        self.cID.grid(column=1,row=2,sticky='EW')

        login = tk.Button(self,text="Login",command=lambda: self.loginCheck())
        login.grid(column=0,row=3)

        bButton = tk.Button(self,text="Go back",command=lambda: controller.show_frame(StartMenu))
        bButton.grid(column=1,row=3)

    def loginCheck(self):
        loggedIn = buyer_login(self.uName.get(),self.cID.get())
        if loggedIn:
            print("SUCCESS")
            print(current_user.get_order_id())
            self.controller.show_frame(BuyerMenu)
            #TODO buyers menu
        else:
            print("FAIL")

class BuyerMenu(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Accept order",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')

        sButton = tk.Button(self,text="Accept contract",command=lambda: self.setup())
        sButton.grid(column=0,row=1)

        bButton = tk.Button(self,text="Logout",command=lambda: self.logout())
        bButton.grid(column=1,row=1)

    def logout(self):
        current_user.logout()
        self.controller.show_frame(StartMenu)

    def setup(self):
        delivery_options(2)
        accpet_delivery()
        self.controller.show_frame(PayOrder)
        print(current_user.get_order_id())

class PayOrder(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Pay order!",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')

        pButton = tk.Button(self,text="Pay contract",command=lambda: self.payContract())
        pButton.grid(column=0,row=1)

        bButton = tk.Button(self,text="Logout",command=lambda: self.logout())
        bButton.grid(column=1,row=3)

    def payContract(self):
        pay()




class NewMember(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller

        self.labelText = tk.StringVar()
        label = tk.Label(self,text="Register member",fg="black",bg="white")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')

        self.fNameLable = tk.Label(self,text="First name:")
        self.fNameLable.grid(column=0,row=1,sticky='EW')
        self.fName = tk.Entry(self)
        self.fName.grid(column=1,row=1,sticky='EW')

        self.lNameLable = tk.Label(self,text="Last name:")
        self.lNameLable.grid(column=0,row=2,sticky='EW')
        self.lName = tk.Entry(self)
        self.lName.grid(column=1,row=2,sticky='EW')

        self.emailLable = tk.Label(self,text="E-mail:")
        self.emailLable.grid(column=0,row=3,sticky='EW')
        self.email = tk.Entry(self)
        self.email.grid(column=1,row=3,sticky='EW')

        self.pWordLable = tk.Label(self,text="Password:")
        self.pWordLable.grid(column=0,row=4,sticky='EW')
        self.pWord = tk.Entry(self,show='*')
        self.pWord.grid(column=1,row=4,sticky='EW')

        self.addressLable = tk.Label(self,text="Address:")
        self.addressLable.grid(column=0,row=5,sticky='EW')
        self.address = tk.Entry(self)
        self.address.grid(column=1,row=5,sticky='EW')

        self.zipLable = tk.Label(self,text="Zip-code:")
        self.zipLable.grid(column=0,row=6,sticky='EW')
        self.zip = tk.Entry(self)
        self.zip.grid(column=1,row=6,sticky='EW')

        self.cityLable = tk.Label(self,text="City:")
        self.cityLable.grid(column=0,row=7,sticky='EW')
        self.city = tk.Entry(self)
        self.city.grid(column=1,row=7,sticky='EW')

        self.brnLable = tk.Label(self,text="Bank routing number:")
        self.brnLable.grid(column=0,row=8,sticky='EW')
        self.brn = tk.Entry(self)
        self.brn.grid(column=1,row=8,sticky='EW')

        self.banLable = tk.Label(self,text="Bank account number:")
        self.banLable.grid(column=0,row=9,sticky='EW')
        self.ban = tk.Entry(self)
        self.ban.grid(column=1,row=9,sticky='EW')

        rCustomerButton = tk.Button(self,text="Register Customer",command=lambda: self.registerCustomer())
        rCustomerButton.grid(column=0,row=10)

        rDriverButton = tk.Button(self,text="Register Driver",command=lambda: self.registerDriver())
        rDriverButton.grid(column=1,row=10)

        bButton = tk.Button(self,text="Go back",command=lambda: controller.show_frame(StartMenu))
        bButton.grid(column=2,row=10,columnspan=1)

    def registerCustomer(self):
        save_user_data(self.fName.get(),self.lName.get(),self.email.get(),hash(self.pWord.get()),self.address.get(),int(self.zip.get()),self.city.get(),int(self.brn.get()),int(self.ban.get()),False)
        self.controller.show_frame(StartMenu)

    def registerDriver(self):
        save_user_data(self.fName.get(),self.lName.get(),self.email.get(),hash(self.pWord.get()),self.address.get(),int(self.zip.get()),self.city.get(),int(self.brn.get()),int(self.ban.get()),True)
        self.controller.show_frame(StartMenu)

if __name__ == "__main__":
    app = GUI()
    app.title('D2D.se')
    app.mainloop()

