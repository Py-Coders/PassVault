#!/bin/python3
import sqlite3
import hashlib
from tkinter import *
from tkinter import simpledialog
from functools import partial
import uuid
import pyperclip #copy recovary key
import base64 #encrypt data
import os
#for fernet for encryption
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet



# database code


with sqlite3.connect("GUI-Database.db") as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
recovaryKey TEXT NOT NULL);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

# Create PopUP


def popUp(text):
    answer = simpledialog.askstring("Input string", text)
    # print(answer)
    return answer

# initiate

window = Tk()

# md-5 Hashing (encryption)

def hashPassword(input):
    hash = hashlib.sha256(input)

    hash = hash.hexdigest()  # decrypt

    return hash


def firstscreen():
    window.geometry("450x200")  # for the size of the interface

    # text above the input box of the master password
    lbl1 = Label(window, text="Create master password : ")
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=0)

    # show = "*") #input box of the masterr password
    txt = Entry(window, width=20)
    txt.pack(pady=4)
    txt.focus()

    # text above re-entering password
    lbl2 = Label(window, text="Re-Enter password for confirmation ")
    lbl2.pack()

    # show = "*") #input box for re-entering password
    txt1 = Entry(window, width=20)
    txt1.pack()
    txt1.focus()

    lbl3 = Label(window)
    lbl3.pack()

    def savePassword():
        if txt.get() == txt1.get():

            sql = "DELETE FROM masterpassword WHERE if = 1"

            cursor.execute(sql)
            hashedPassword = hashPassword(txt.get().encode("utf-8"))

            key = str(uuid.uuid4().hex)

            recoveryKey = hashPassword(key.encode('utf-8'))

            insert_password = """ INSERT INTO masterpassword(password, recovaryKey)
            VALUES(?, ?)"""
            cursor.execute(insert_password, ((hashedPassword), (recoveryKey)))
            db.commit()

            recoveryScreen()
        else:
            lbl3.config(text="Password do not match")

    # button for submitting the master password
    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=6)



def recoveryScreen(key):


    window.geometry("450x200")  # for the size of the interface

    # text above the input box of the master password
    lbl1 = Label(window, text="Save this key to recover account : ")
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=0)

    # text above re-entering password
    lbl2 = Label(window, text="key")
    lbl2.pack()

    lbl3 = Label(window)
    lbl3.pack()

    def copyKey():
        pyperclip.copy

    def savePassword():
        if txt.get() == txt1.get():

            sql = "DELETE FROM masterpassword WHERE if = 1"

            cursor.execute(sql)
            hashedPassword = hashPassword(txt.get().encode("utf-8"))

            key = str(uuid.uuid4().hex)

            recoveryKey = hashPassword(key.encode('utf-8'))

            insert_password = """ INSERT INTO masterpassword(password, recovaryKey)
            VALUES(?, ?)"""
            cursor.execute(insert_password, ((hashedPassword), (recoveryKey)))
            db.commit()

            recoveryScreen()
        else:
            lbl3.config(text="Password do not match")

    # button for submitting the master password
    btn = Button(window, text="Save", command=savePassword)
    btn.pack(pady=6)




window.title("Password Box")


def loginScreen():
    window.geometry("450x250")  # for the size of the interface

    # for the name of the GUI interface
    lbl1 = Label(window, text="Enter the Master Password : ")
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=0)

    lbl2 = Label(window)  # for the name of the GUI interface
    lbl2.pack()

    # for the Master Pasword input area text
    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    def getMasterPassword():
        checkHashedPassword = hashPassword(txt.get().encode("utf-8"))
        cursor.execute(
            "SELECT * FROM masterpassword WHERE id = 1 AND password = ? ", [(checkHashedPassword)])
        print(checkHashedPassword)
        return cursor.fetchall()

    def checkpassword():
        # print("test")
        match = getMasterPassword()

        print(match)

        if match:
            lbl2.config(text="Right Password")
            passwordvault()

        else:
            txt.delete(0, "end")
            lbl2.config(text="Wrong Password")

    # button for submitting the master password
    btn = Button(window, text="SUBMIT", command=checkpassword)
    btn.pack(pady=6)


def passwordvault():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"

        website = popUp(text1)
        username = popUp(text2)
        password = popUp(text3)

        insert_fields = """INSERT INTO vault(website, username, password)
        VALUES(?,?,?)"""

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        passwordvault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()
        passwordvault()

    window.geometry("700x350")

    #popUp("Whats your name ?")

    lbl = Label(window, text="Password Vault")
    lbl.grid(column=1)

    btn = Button(window, text="+", command=addEntry)
    btn.grid(column=1, pady=10)

    lbl = Label(window, text="Website")
    lbl.grid(row=2, column=0, padx=88)
    lbl = Label(window, text="username")
    lbl.grid(row=2, column=1, padx=88)
    lbl = Label(window, text="Password")
    lbl.grid(row=2, column=2, padx=88)

    cursor.execute("SELECT * FROM vault")
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute("SELECT * FROM vault")
            array = cursor.fetchall()

            # website
            lbl1 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl1.grid(column=0, row=i+3)
            # Username
            lbl1 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl1.grid(column=1, row=i+3)
            # password
            lbl1 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl1.grid(column=2, row=i+3)

            # partial is used to delete the mentioned or the requested column only
            btn = Button(window, text="Delete",
                         command=partial(removeEntry, array[i][0]))
            btn.grid(column=4, row=i+3, pady=10)

            i += 1

            cursor.execute("SELECT * FROM vault")
            if (len(cursor.fetchall()) <= i):
                break


# firstscreen()

cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen()
else:
    firstscreen()


window.mainloop()

# last timestamp -> part 2 complete
# link = https://youtu.be/UrH2WCoYEVo
