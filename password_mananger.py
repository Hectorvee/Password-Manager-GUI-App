import tkinter
import random
import pyperclip
from tkinter import messagebox
import json


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search():
    """Search for and display the password for a given website."""
    website = website_entry.get().lower()  # Get the website name from the entry and convert to lowercase

    if len(website) == 0:
        messagebox.showerror(title="Oops!",
                             message="You need to enter the name of the website you are trying to search")
        return

    try:
        # Attempt to open and read the JSON file
        with open("database/password_info.json", "r") as file:
            data = json.load(file)
            try:
                # Retrieve the username and password for the website
                username = data[website]["username"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
            except KeyError:
                # Handle the case where the website is not found in the data
                messagebox.showerror(title="Oops", message=f"Data for {website} not found")
    except FileNotFoundError:
        # Handle the case where the file does not exist
        messagebox.showerror(title="Error", message="No file found")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    """Generate a random password and display it in the password entry field."""
    password_entry.delete(0, tkinter.END)  # Clear any existing text in the password entry field
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")  # List of letters
    numbers = list("1234567890")  # List of numbers
    symbols = list("!@#$%&*()_?")  # List of symbols
    password = []

    # Generate random counts for each type of character
    nr_letters = random.randint(8, 10)
    nr_numbers = random.randint(2, 5)
    nr_symbols = random.randint(2, 4)

    # Add random characters to the password list
    password += [random.choice(letters) for _ in range(nr_letters)]
    password += [random.choice(numbers) for _ in range(nr_numbers)]
    password += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password)  # Shuffle the characters to randomize the order
    password = "".join(password)  # Convert the list to a string
    password_entry.insert(tkinter.END, string=password)  # Insert the generated password into the entry field
    # pyperclip.copy(password)  # Uncomment to copy the password to the clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    """Save the entered website, username, and password to the JSON file."""
    website = website_entry.get().lower()  # Get the website name
    username = username_entry.get()  # Get the username
    password = password_entry.get()  # Get the password

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops!", message="Please don't leave any fields empty!")
    else:
        # Confirm with the user before saving
        is_okay = messagebox.askokcancel(title=website,
                                         message=f"These are the details entered:\nusername: {username}\npassword: {password}\n\nIs it okay to save?")
        new_data = {
            website: {
                "username": username,
                "password": password
            }
        }

        if is_okay:
            try:
                with open("database/password_info.json", "r") as file:
                    # Read existing data from the file
                    data = json.load(file)

                    if website in data:
                        # Handle the case where the website already exists in the data
                        messagebox.showerror(title="Error!", message=f"{website} is already in the database")
                        return

                    # Update the data with the new entry
                    data.update(new_data)
            except FileNotFoundError:
                with open("database/password_info.json", "w") as file:
                    # Create a new file and write the new data
                    json.dump(new_data, file, indent=4)
            else:
                with open("database/password_info.json", "w") as file:
                    # Save the updated data to the file
                    json.dump(data, file, indent=4)

            messagebox.showinfo(title="Saved", message=f"Added {website} to the data store")
            website_entry.delete(0, "end")  # Clear the website entry field
            password_entry.delete(0, "end")  # Clear the password entry field
            website_entry.focus()  # Set focus back to the website entry field


# ---------------------------- UI SETUP ------------------------------- #

# Create the main window
window = tkinter.Tk()
window.title("Password Manager")  # Set the window title
window.config(padx=20, pady=20)  # Add padding around the window

# UI Elements
canvas = tkinter.Canvas(width=200, height=200)  # Create a canvas for the logo
lock_img = tkinter.PhotoImage(file="images/logo.png")  # Load the logo image
canvas.create_image(100, 100, image=lock_img)  # Add the logo image to the canvas
canvas.grid(column=1, row=0)  # Position the canvas in the grid

# Labels
website_label = tkinter.Label(text="Website:")
website_label.grid(column=0, row=1)

username_label = tkinter.Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = tkinter.Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = tkinter.Entry(width=28)  # Entry for the website name
website_entry.focus()  # Set focus to this entry field
website_entry.grid(column=1, row=1)

username_entry = tkinter.Entry(width=52)  # Entry for the username
username_entry.insert(tkinter.END, string="vukosi1632@gmail.com")  # Default value for the username
username_entry.grid(column=1, row=2, columnspan=2)

password_entry = tkinter.Entry(width=28)  # Entry for the password
password_entry.grid(column=1, row=3)

# Buttons
generate_pass_btn = tkinter.Button(text="Generate Password", width=20,
                                   command=generate_password)  # Button to generate a password
generate_pass_btn.grid(column=2, row=3)

add_btn = tkinter.Button(text="Add", width=49, command=save)  # Button to save the password
add_btn.grid(column=1, row=4, columnspan=2)

search_btn = tkinter.Button(text="Search", width=20, command=search)  # Button to search for a password
search_btn.grid(column=2, row=1)

# Run the application
window.mainloop()
