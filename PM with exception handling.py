from tkinter import *
from tkinter import messagebox
from random import randint
from random import shuffle
from random import choice
import pyperclip
import json


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():

    letter_list=[choice(letters) for _ in range(randint(8,9))]
    symbol_list=[choice(symbols) for _ in range(randint(1,2))]
    number_list=[choice(numbers) for _ in range(randint(1,2))]

    password_list=letter_list+symbol_list+number_list
    shuffle(password_list)

    password="".join(password_list)

    passwordEntry.delete(0, 'end')
    passwordEntry.insert(0, password)

    pyperclip.copy(password)

# ---------------------------- Verify All Info ------------------------------- #

def check_info():
    website = websiteEntry.get()
    username = emailEntry.get()
    password = passwordEntry.get()

    infoList=[website, username, password]
    emptyFields = []

    for x in infoList:
        print(x)
        if x == "":
            emptyFields.append(x)

    if len(emptyFields) > 0:
        woahThere=messagebox.showwarning(title="Whoopsies", message="Cannot save password with missing information")

    else:
        confirmation = myBox = messagebox.askokcancel(title="website", message=f"Here are the details entered:\n\n"
                                                                           f"username: {username}\n"
                                                                           f"password: {password}\n\n"
                                                                           f"Ready to save?")
        if confirmation == True:
            save_data()



def save_data():
    website = websiteEntry.get()
    username = emailEntry.get()
    password = passwordEntry.get()

    newdata = {
        website:{
            "email":username,
            "password":password
        }
    }


    with open("data.json","r") as data_file:

        try:
            current_data = json.load(data_file)
            current_data.update(newdata)
        except:
            current_data=newdata

        finally:
            with open("data.json", "w") as data_file:
                json.dump(current_data, data_file, indent=1)


    websiteEntry.delete(0, 'end')
    emailEntry.delete(0,'end')
    passwordEntry.delete(0, 'end')
# ---------------------------- UI SETUP ------------------------------- #

def find_password():
    website=websiteEntry.get()

    with open("data.json", "r") as datafile:
        try:
            data=json.load(datafile)

        except AttributeError:
            nodata=messagebox.showinfo(title="Data not found", message="No passwords have been saved yet.")

        else:
            try:

                username=data[website]["email"]
                password=data[website]["password"]
                print(f"Username/email for {website}: {username}")
                print(f"Password for {website}: {password}")
            except KeyError:
                nodata = messagebox.showinfo(title="Data not found", message="This website has not been registered yet")


# ---------------------------- SAVE PASSWORD ------------------------------- #

window=Tk()
window.title("Password Manager")
window.configure( padx=20, pady=20)

canvas=Canvas(width=150, height=200, highlightthickness=0)
logo=PhotoImage(file="logo.png")
canvas.create_image(75,100, image=logo)

websiteLabel=Label(window, text="Website:")
emailLabel=Label(window, text="Email/Username:")
PasswordLabel=Label(window, text="Password:")
websiteEntry=Entry(window, width=20)
websiteEntry.focus()
emailEntry=Entry(window, width=39)
passwordEntry=Entry(window, width=20)
searchButt=Button(window, text="Search", command=find_password)
generateButt=Button(window, text="Generate Password", command=password_generator)
addButt=Button(window, text="Add", width=33, command=save_data)


canvas.grid(row=0,column=1)
websiteLabel.grid(row=1, column=0)
emailLabel.grid(row=2,column=0)
PasswordLabel.grid(row=3,column=0)
websiteEntry.grid(row=1, column=1)
emailEntry.grid(row=2, column=1, columnspan=2)
passwordEntry.grid(row=3, column=1)
searchButt.grid(row=1, column=2)
generateButt.grid(row=3, column=2)
addButt.grid(row=4, column=1, columnspan=2)

window.mainloop()