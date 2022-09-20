import tkinter
import random
import pyperclip
from tkinter import messagebox
import json


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search():
    
    website = website_entry.get().lower()

    if len(website) == 0:
        messagebox.showerror(title="Oops!", message="You need to enter the name of the webstite you are trying to seacrh")
        return
    
    try:
        with open("password_info.json", "r") as file:
            data = json.load(file)
            try:
                username = data[website]["username"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
            except KeyError:
                messagebox.showerror(title="Oops", message=f"Data for {website} not found")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No file found")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():

    password_entry.delete(0,tkinter.END)
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ")
    numbers = list("1234567890")
    symbols = list("!@#$%&*()_?")
    password = []

    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 5)
    nr_symbols = random.randint(2, 4)

    password += [random.choice(letters) for _ in range(nr_letters)]
    password += [random.choice(numbers) for _ in range(nr_numbers)]
    password += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password)
    password = "".join(password)
    password_entry.insert(tkinter.END, string=password)
    # pyperclip.copy(password)

    

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website = website_entry.get().lower()
    username = username_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops!", message="Please don't leave any fields empty!")
    else:
        is_okay = messagebox.askokcancel(title=website, message=f"These are the details entered:\nusername: {username}\npassword: {password}\n\nIs it okay to save?")
        new_data = {
            website: {
                "username": username,
                "password": password
            }
        }

        if is_okay:
            try:
                with open("password_info.json", "r") as file:
                    # Reading old data
                    data = json.load(file)

                    if website in data:
                        messagebox.showerror(title="Error!", message=f"{website} is already in the database")
                        return
                    
                    # Updating old data with new data
                    data.update(new_data)
            except FileNotFoundError:
                with open("password_info.json", "w") as file:
                    # Opening a new file
                    json.dump(new_data, file, indent=4)
            else:
                with open("password_info.json", "w") as file:
                    # Saving updated data
                    json.dump(data, file, indent=4)
            
            messagebox.showinfo(title="Saved", message=f"Added {website} to the data store")
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")
            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.title("Password Mananger")
window.config(padx=20, pady=20)

# UI
canvas = tkinter.Canvas(width=200, height=200)
lock_img = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)


# Labels
website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1)

username_label = tkinter.Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3)


# Entries
website_entry = tkinter.Entry(width=28)
website_entry.focus()
website_entry.grid(column=1, row=1)

username_entry = tkinter.Entry(width=52)
username_entry.insert(tkinter.END, string="vukosi1632@gmail.com")
username_entry.grid(column=1, row=2, columnspan=2)

password_entry = tkinter.Entry(width=28)
password_entry.grid(column=1, row=3)


# Buttons
generate_pass_btn = tkinter.Button(text="Generate Password", width=20, command=generate_password)
generate_pass_btn.grid(column=2, row=3)

add_btn = tkinter.Button(text="Add", width=49, command=save)
add_btn.grid(column=1, row=4, columnspan=2)

search_btn = tkinter.Button(text="Search", width=20, command=search)
search_btn.grid(column=2, row=1)



window.mainloop()
