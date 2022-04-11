#!/bin/python3
import sqlite3
import hashlib
import os
from tkinter import *
from tkinter import simpledialog
from functools import partial
import uuid
import pyperclip
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet


backend = default_backend()
salt = b'2444'

kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=backend
)

encryptionKey = 0


def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)


def decrypt(message: bytes, token: bytes) -> bytes:
    return Fernet(token).decrypt(message)


# database code
with sqlite3.connect('password_vault.db') as db:
    cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS masterpassword(
id INTEGER PRIMARY KEY,
password TEXT NOT NULL,
recoveryKey TEXT NOT NULL);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vault(
id INTEGER PRIMARY KEY,
website TEXT NOT NULL,
username TEXT NOT NULL,
password TEXT NOT NULL);
""")

# PassVault LOGO :)
'''def icon():
    app = Tk()
    app.iconbitmap(r'C:\All Files\Source codes\Password Database\PassVault 2.0\passLogo.ico')
    app.mainloop() '''


# Create PopUp
def popUp(text):
    answer = simpledialog.askstring("input string", text)

    return answer


# Opening window
window = Tk()
window['background'] = '#89dcc7'

window.update()

window.title("PassVault")  # This is the opening screen's title of the window


def hashPassword(input):
    hash1 = hashlib.sha256(input)
    hash1 = hash1.hexdigest()

    return hash1


def firstTimeScreen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry('450x250')

    # icon()

    lbl = Label(window, text="Create a  Password", font=('Times', 20, 'bold'), bg="#89dcc7")  # showing text
    lbl.config(anchor=CENTER)  # position
    lbl.pack(pady=5)

    txt = Entry(window, width=20, font=20, show="*")  # input
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text="Re-enter password", font=('Times', 20, 'bold'), bg="#89dcc7")
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=5)

    txt1 = Entry(window, width=20, font=20, show="*")
    txt1.pack()

    def savePassword():
        if txt.get() == txt1.get():
            sql = "DELETE FROM masterpassword WHERE id = 1"

            cursor.execute(sql)

            # Recovary Key

            hashedPassword = hashPassword(txt.get().encode('utf-8'))
            key = str(uuid.uuid4().hex)
            recoveryKey = hashPassword(key.encode('utf-8'))

            global encryptionKey

            encryptionKey = base64.urlsafe_b64encode(
                kdf.derive(txt.get().encode()))

            insert_password = """INSERT INTO masterpassword(password, recoveryKey) VALUES(?, ?) """
            cursor.execute(insert_password, ((hashedPassword), (recoveryKey)))
            db.commit()

            recoveryScreen(key)
        else:
            lbl.config(text="Passwords dont match")

    btn = Button(window, text="Save", command=savePassword, font=('Times', 15, 'bold'))
    btn.pack(pady=8)


def recoveryScreen(key):
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry('700x300')
    lbl = Label(window, text="Copy and save this key to recover account later onn", font=('Times', 20, 'bold'), bg="#89dcc7")
    lbl1 = Label(window, text="Itne jaldi bhul gayee ?", font=('Times', 20, 'bold'), bg="#89dcc7")
    lbl.config(anchor=CENTER)
    lbl.pack(pady=5)

    lbl1 = Label(window, text=key, font=('Roboto', 15, 'bold'), bg='#ccffff')
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=5)

# This provides the account recovery key

    def copyKey():
        pyperclip.copy(lbl1.cget("text"))

    btn = Button(window, text="Copy Key", font=('Times', 15, 'bold'), command=copyKey)
    btn.pack(pady=5)

    def done():
        menu()
        # vaultScreen()

    btn = Button(window, text="Done", font=('Times', 15, 'bold'), command=done)
    btn.pack(pady=5)


def resetScreen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry('450x150')
    lbl = Label(window, text="Enter Recovery Key", bg="#89dcc7", font=('Times', 20, 'bold'))
    lbl.config(anchor=CENTER)
    lbl.pack(pady=10)

    txt = Entry(window, width=20)
    txt.pack()
    txt.focus()

    """ lbl1 = Label(window)
    lbl1.config(anchor=CENTER)
    lbl1.pack() """

    # This will check that the revocary key is correct or not

    def getRecoveryKey():
        recoveryKeyCheck = hashPassword(str(txt.get()).encode('utf-8'))
        cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND recoveryKey = ?', [(recoveryKeyCheck)])
        return cursor.fetchall()

    def checkRecoveryKey():
        checked = getRecoveryKey()

        if checked:
            firstTimeScreen()
        else:
            txt.delete(0, 'end')
            lbl.config(text='Wrong Key')

    btn = Button(window, text="Check Key", font=('Times', 10, 'bold'), command=checkRecoveryKey)
    btn.pack(pady=5)


def loginScreen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry('500x250')

    lbl = Label(window, text="Enter  Master Password", font=('Times', 20, 'bold'), bg="#89dcc7")
    lbl.config(anchor=CENTER)
    lbl.pack(pady=25)

    txt = Entry(window, width=30, show="*_*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window, bg="#89dcc7")
    lbl1.config(anchor=CENTER)
    lbl1.pack(side=TOP)

    def getMasterPassword():
        checkHashedPassword = hashPassword(txt.get().encode('utf-8'))
        global encryptionKey
        encryptionKey = base64.urlsafe_b64encode(kdf.derive(txt.get().encode()))
        cursor.execute('SELECT * FROM masterpassword WHERE id = 1 AND password = ?', [(checkHashedPassword)])
        return cursor.fetchall()

    def checkPassword():
        password = getMasterPassword()

        print(password)  # proof that it's getting hashed in the database

        if password:
            menu()
            # vaultScreen()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Password", font=('Times', 10, 'bold'))

            btn = Button(window, text="Reset Password", command=resetPassword)
            btn.pack(pady=5)

    def resetPassword():
        resetScreen()

    btn = Button(window, text="Enter", font=('Consolas', 12, 'bold'), command=checkPassword)
    btn.pack(pady=5)

    #btn = Button(window, text="Reset Password", command=resetPassword)
    # btn.pack(pady=5)


def menu():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry('250x200')

    lbl = Label(window, text=" What you want to do ? ", bg="#89dcc7", font=('Helvetica', 10, 'bold'))
    lbl.config(anchor=CENTER)
    lbl.grid(row=1, column=0, padx=50, pady=5)

    def addPassword():
        addpass()

    btn = Button(window, text="Add Password", command=addPassword)
    btn.grid(row=3, column=0, padx=50, pady=5)

    def ShowPassword():
        showpass()

    btn = Button(window, text="Manage Passwords", command = ShowPassword)
    btn.grid(row=5, column=0, padx=50, pady=5)

    btn = Button(window, text="Delete the user", command = vaultDel)
    btn.grid(row=11, column=0, padx=50, pady=5)


def vaultScreen():
    for widget in window.winfo_children():
        widget.destroy()

    

    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"
        website = encrypt(popUp(text1).encode(), encryptionKey)
        username = encrypt(popUp(text2).encode(), encryptionKey)
        password = encrypt(popUp(text3).encode(), encryptionKey)

        insert_fields = """INSERT INTO vault(website, username, password) VALUES(?, ?, ?) """
        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        
        vaultScreen()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()
        vaultScreen()
    
    def copyPass():
        pyperclip.copy(lbl1.cget("password"))

    window.geometry('1000x550')
    window.resizable(height=None, width=None)
    lbl = Label(window, text="Password Vault", font=("Times", 20, 'bold'))
    lbl.grid(column=1)
    btn = Button(window, text="Go back to Menu", command=menu)
    btn.grid(column=1, pady=10)

    #btn = Button(window, text="+", command=addEntry)
    #btn.grid(column=1, pady=10)

    lbl = Label(window, text="Website", font=("Helvetica", 12, 'bold'))
    lbl.grid(row=2, column=0, padx=90)
    lbl = Label(window, text="Username", font=("Helvetica", 12, 'bold'))
    lbl.grid(row=2, column=1, padx=90)
    lbl = Label(window, text="Password", font=("Helvetica", 12, 'bold'))
    lbl.grid(row=2, column=2, padx=90)

    cursor.execute('SELECT * FROM vault')
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute('SELECT * FROM vault')
            array = cursor.fetchall()

            if (len(array) == 0):
                break

            lbl1 = Label(window, text=(decrypt(array[i][1], encryptionKey)), font=("Helvetica", 12))
            lbl1.grid(column=0, row=(i+3))
            lbl2 = Label(window, text=(decrypt(array[i][2], encryptionKey)), font=("Helvetica", 12))
            lbl2.grid(column=1, row=(i+3))
            lbl3 = Label(window, text=(decrypt(array[i][3], encryptionKey)), font=("Helvetica", 12))
            lbl3.grid(column=2, row=(i+3))

            btn = Button(window, text="Delete", command=partial(removeEntry, array[i][0]))
            btn.grid(column=3, row=(i+3), pady=10)

            btn = Button(window, text="Copy Key", command = copyPass)
            btn.grid(column=4, row=(i+3), pady=10)
            
            
            
            i = i + 1

            cursor.execute('SELECT * FROM vault')
            if (len(cursor.fetchall()) <= i):
                break


def addpass():

    for widget in window.winfo_children():
        widget.destroy()
    
    window['background'] = '#89dcc7'

    def addEntry():
        
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"
        website = encrypt(popUp(text1).encode(), encryptionKey)
        username = encrypt(popUp(text2).encode(), encryptionKey)
        password = encrypt(popUp(text3).encode(), encryptionKey)

        insert_fields = """INSERT INTO vault(website, username, password) 
        VALUES(?, ?, ?) """
        cursor.execute(insert_fields, (website, username, password))
        db.commit()
        lbl = Label(window, text=" Your Credentials saved securely.", font=('Times', 20, 'bold'))
        lbl.config(anchor=CENTER)
        #lbl.pack(pady=25)

        addpass()

    # def removeEntry(input):
        #cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        # db.commit()
        # vaultScreen()

    window.geometry('300x150')
    window.resizable(height=None, width=None)
    lbl = Label(window, text="Password Vault", bg='#89dcc7', font=('Times', 30, 'bold'))
    lbl.grid(column=1, pady=5)

    btn2 = Button(window, text="Go back to Menu", command=menu)
    btn2.grid(row=1, column=1)

    btn = Button(window, text="Add Credentials", command=addEntry)
    btn.grid(column=1, pady=10)

def showpass():
    for widget in window.winfo_children():
        widget.destroy()

    window['background'] = '#89dcc7'

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()
        vaultScreen()

    def addEntry():
        text1 = "Website"
        text2 = "Username"
        text3 = "Password"
        website = encrypt(popUp(text1).encode(), encryptionKey)
        username = encrypt(popUp(text2).encode(), encryptionKey)
        password = encrypt(popUp(text3).encode(), encryptionKey)

        insert_fields = """INSERT INTO vault(website, username, password) 
        VALUES(?, ?, ?) """
        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        #temporary trial for delete of password 

        cursor.execute('SELECT * FROM vault')
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute('SELECT * FROM vault')
            array = cursor.fetchall()

            if (len(array) == 0):
                break

            lbl1 = Label(window, text=(decrypt(array[i][1], encryptionKey)), font=("Helvetica", 12))
            lbl1.grid(column=0, row=(i+4), pady = 5)
            lbl2 = Label(window, text=(decrypt(array[i][2], encryptionKey)), font=("Helvetica", 12))
            lbl2.grid(column=1, row=(i+4), pady = 5)
            lbl3 = Label(window, text=(decrypt(array[i][3], encryptionKey)), font=("Helvetica", 12))
            lbl3.grid(column=2, row=(i+4), pady = 5)

            btn = Button(window, text="Delete", command=  partial(removeEntry, array[i][0]))
            btn.grid(column=3, row=(i+3), pady=10)
            btn2 = Button(window, text="Go back to Menu", command=menu)
            btn2.grid(column=1, pady=10)

            i = i +1

            cursor.execute('SELECT * FROM vault')
            if (len(cursor.fetchall()) <= i):
                break

        vaultScreen()

'''
                    DELETE DATABASE
'''

def vaultDel():
    for widget in window.winfo_children():
        widget.destroy()
    window.geometry('550x350')
    
    def delDB():
        for widget in window.winfo_children():
            widget.destroy()
        window.geometry('550x350')
        lbl = Label(window, text="Delete PassVault", bg='#89dcc7', font=('Times', 30, 'bold'))
        lbl.config(anchor=CENTER)  # position
        lbl.pack(pady=5)
        lbl1 = Label(window, text="Deletion completed succesfully.",bg='#89dcc7', font=("Helvetica", 12))
        lbl1.config(anchor=CENTER)  # position
        lbl1.pack(pady=5) 
        os.system("del /f password_vault.db")
    lbl = Label(window, text="Delete PassVault", bg='#89dcc7', font=('Times', 30, 'bold'))
    lbl.config(anchor=CENTER)  # position
    lbl.pack(pady=5)
    btn2 = Button(window, text="Sure you want to delete ?", command=delDB)
    btn2.config(anchor=CENTER)  # position
    btn2.pack(pady=5)
    
    

cursor.execute('SELECT * FROM masterpassword')
if (cursor.fetchall()):
    loginScreen()
else:
    firstTimeScreen()
window.mainloop()
