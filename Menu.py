import random #for random number 
root="Test"
dic={"ayanm":"1234","roshm":"5678"} #format-username:password
cnt1=3
cnt2=3
cnt3=3
cnt4=0
s="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%123456789"
lst=list(s)
def usernamegen(name):
    global dic
    global lst
    namer=name
    for i in range(5):
        r1=random.choice(lst)
        namer+=r1
    #print("ok")
    if namer in dic.keys():
        usernamegen(name)
    else:
        return namer
def passwordgen():
    global lst
    r3=""
    r2=random.randint(10,15)
    for i in range(r2):
        r4=random.choice(lst)
        r3+=r4
    return r3
while cnt1>0:
    a=input("Enter root password for database:- ")
    if a==root:
        print("Access granted for database.")
        b=input("Are you a registered user? (y/n)")
        if b in "yesYESYes":
            while cnt2>0:
                b=input("Enter your username:- ")
                if b in dic.keys():
                    while cnt3>0:
                        c=input("Enter password:- ")
                        if c==dic[b]:
                            print("Access granted for username:-",b)
                            cnt4=1
                            break
                        else:
                            cnt3-=1
                            print("Wrong password.",cnt3,"tries left.")
                    break
                else:
                    cnt2-=1
                    print("Username doesn't exist.",cnt2,"tries left.")
        elif b in "noNONo":
            print("You have to create a username.")
            c=input("Enter your first name:- ")
            #print("Here are some suggestions:- ")
            #for i in range(5):
            #    d=usernamegen(c)
            #    print(d)
            while True:
                e=input("Enter your username:- ")
                if e in dic.keys():
                    print("This username has already been taken away by somebody else. Re-enter another username.")
                else:
                    print("You need to give a password.")
                    print("Here are some suggestions:- ")
                    for i in range(5):
                        f=passwordgen()
                        print(f)
                    g=input("Enter your password:- ")
                    dic[e]=g
                    print("USER ACCOUNT created successfully.")
                    print("Access granted for username:-",e)
                    cnt4=1
                    break
        else:
            print("Error occurred.")
        break
    else:
        cnt1-=1
        print("Wrong password.",cnt1,"tries left.")
if cnt4==1:
    print("Type out the number that is associated with the work you want to do from the following options:- ")
    while True:
        try:
            print("1. Add new username and password for a website/application to the database.\n2. Generate a random and secured password.\n3. Retrieve password from the database.\n4. Update the existing password from the database.\n5. List out all the accounts/websites that are using same password.\n6. Display all the details stored in the database to the user.\n7. Exit")
            p=int(input("Enter your choice:- "))
            if p==1:
                q=input("Enter the name of the website/application:- ")
                r=input("Enter the USERNAME/USER ID :- ")
                sug = input("Do you want password suggestion y/n ? : ")
                if sug in "yesYESYes":
                    for i in range(10):
                        t=passwordgen()
                        print(t)
                        s=input("Enter the PASSWORD:- ")
                elif sug in "noNONo":
                    s=input("Enter the PASSWORD:- ")
                print("Data added successfuly.")
            elif p==2:
                for i in range(10):
                    t=passwordgen()
                    print(t)
            elif p==3:
                q=input("Enter the name of the website/application:- ")
                r=input("Enter the USERNAME/USER ID :- ")
                print("Password retrieved successfully.")
            elif p==4:
                q=input("Enter the name of the website/application:- ")
                r=input("Enter the USERNAME/USER ID :- ")
                print("OLD PASSWORD")
                #print("Here are some passwords (suggestions):- ")
                #for i in range(10):
                #    t=passwordgen()
                #    print(t)
                s=input("Enter new password:- ")
                print("Password updated successfully.")
            elif p==5:
                q=input("Enter the PASSWORD:- ")
                print("SHOWING ALL THE ACCOUNTS/WEBSITES USING THE SAME PASSWORD.")
            elif p==6:
                print("SHOWING ALL THE DATA TO THE USER.")
            elif p==7:
                break
            else:
                print("There is no such choice. Re-enter your choice carefully.")
        except:
            print("There is no such choice. Re-enter your choice carefully.")
            continue    