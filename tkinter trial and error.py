from tkinter import *

window = Tk()
window.update()
window.title("Trial and Error")


for widget in window.winfo_children():
    widget.destroy()

# _________________Code snippet for MENU ___________________

window.geometry('250x200')

lbl = Label(window, text=" What you want to do ? ", font = ('Helvetica', 10, 'bold'))
lbl.config(anchor =CENTER)
lbl.grid(row=1, column=0, padx = 50, pady = 5)

#lbl = Label(window, text="Add Password")
#lbl.grid(row=2, column=0, padx = 50, pady = 5)
btn = Button(window, text="Add Password")
btn.grid(row=3, column=0, padx = 50, pady = 5)

#lbl = Label(window, text="Show password")
#lbl.grid(row=4, column=0, padx = 50, pady = 5)
btn = Button(window, text="Show all Passwords")
btn.grid(row=5, column=0, padx = 50, pady = 5)

#lbl = Label(window, text="List passwords")
#lbl.grid(row=6, column=0, padx = 50, pady = 5)
#btn = Button(window, text="List")
#btn.grid(row=7, column=0, padx = 50, pady = 5)

#lbl = Label(window, text="Update password")
#lbl.grid(row=8, column=0, padx = 50, pady = 5)
btn = Button(window, text="Update password")
btn.grid(row=9, column=0, padx = 50, pady = 5)

#lbl = Label(window, text="Delete User")
#lbl.grid(row=10, column=0, padx = 50, pady = 5)
btn = Button(window, text="Delete the user")
btn.grid(row=11, column=0, padx = 50, pady = 5) 
# ______________________________________________________________________#

#_____________Code snippet for Password ADDING_________________#




window.mainloop()