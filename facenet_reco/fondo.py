from tkinter import *
from tkinter.ttk import * 

root = Tk()

s = Style()
s.configure('My.TFrame', background='red')

mail1 = Frame(root, style='My.TFrame')
mail1.place(height=70, width=400, x=83, y=109)
mail1.config()
root.mainloop()
