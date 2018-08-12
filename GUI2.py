__author__ = 'pierrerudin'

from tkinter import *

tk = Tk()
f = Frame(tk)

# fill frame with 10 buttons
for i in range(10):
    but = Button(f, text=str(i))
    but.grid(column=0,row=i)

# kill the frame and buttons
#f.destroy() # references to buttons gone too, so they are GC'd

# make a new frame and put it in tk
f = Frame(tk)

f.mainloop()