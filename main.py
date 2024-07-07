from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SYMBOLS = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


# ------------------------- SEARCH SAVED PASSWORDS -------------------------------#


def find_password():
    website = website_name.get().title()
    try:
        file = open("passwords.json", 'r')
        file.close()
    except FileNotFoundError:
        messagebox.showerror(title="Website not found!", message="No passwords are saved")
    else:
        with open("passwords.json", 'r') as file:
            data = json.load(file)
            if website not in data:
                messagebox.showerror(title="Website not found!", message=f"The password for {website} is not saved")
            else:
                messagebox.showinfo(title=website, message=f"Username: {data[website]['email']}" 
                                                           f"\nPassword: {data[website]['password']}" 
                                                           f"\nPassword copied to clipboard!")
                website_name.delete(0, END)
                pyperclip.copy(data[website]["password"])
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(LETTERS) for _ in range(nr_letters)]
    password_list += [random.choice(SYMBOLS) for _ in range(nr_symbols)]
    password_list += [random.choice(NUMBERS) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_name.delete(0, END)
    password_name.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_to_file():
    website = website_name.get().title()
    email = email_name.get()
    password = password_name.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }
    if website == "":
        messagebox.showwarning(title="Missing Website", message="Please enter a website name")
    elif password == "":
        messagebox.showwarning(title="Missing Password", message="Please generate a password before adding")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}"
                                                              f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            try:
                open("passwords.json", 'r')
            except FileNotFoundError:
                with open("passwords.json", 'w') as file:
                    json.dump(new_data, file, indent=4)
            else:
                with open("passwords.json", 'r') as file:
                    # Read old data
                    data = json.load(file)
                    # Update old data with new one
                    data.update(new_data)
                    # because read mode cant write new data in .json file
                with open("passwords.json", 'w') as file:
                    json.dump(data, file, indent=4)
        website_name.delete(0, END)
        password_name.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=photo)
canvas.grid(row=0, column=1)

# Website region
website_name = Entry(width=30)
website_name.grid(row=1, column=1)
website_name.focus()
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
search_button = Button(text="Search", width=20, command=find_password)
search_button.grid(row=1, column=2)

# Email/Username region
email_name = Entry(width=55)
email_name.grid(row=2, column=1, columnspan=2)
email_name.insert(END, string="sankalp19june@gmail.com")
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

# Password region
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
password_name = Entry(width=30)
password_name.grid(row=3, column=1)
generate = Button(text="Generate Password", width=20, command=generate_password)
generate.grid(row=3, column=2)

# add button
add_button = Button(text="Add", width=45, command=add_to_file)
add_button.grid(row=4, column=1, columnspan=2)
window.mainloop()
