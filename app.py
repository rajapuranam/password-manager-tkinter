from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle, sample
from pyperclip import copy
from json import load, dump
import hash_password as hp
import os

def search_password():
	website = website_entry.get().lower()
	if len(website) == 0:
		messagebox.showwarning(title="Oops!!", message='Please fill Website field!!')
		return 

	with open('passwords.json', 'r') as file:
		data = load(file)
		creds = data.get(website, -1)
		if creds == -1:
			msg = f"You don't have any saved credentials for {website.capitalize()}"
			messagebox.showwarning(title="Oops!!", message=msg)

		email_entry.delete(0, END)
		email_entry.insert(0, creds['email'])
		password_entry.delete(0, END)
		if hash_password.get() == 1:
			password_entry.insert(0, hp.decrypt(creds['password']))
		else:
			password_entry.insert(0, creds['password'])

def generate_password():
	letters = "".join([chr(97+i) for i in range(26)])
	letters_small = list(letters)
	letters = letters.upper()
	letters_capital = list(letters)
	numbers = [str(i) for i in range(10)]
	symbols = ['!', '#', '$', '%', '&', '@']
	password_list = letters_small+letters_capital+numbers+symbols
	password = "".join(sample(password_list,20))
	password_entry.delete(0, END)
	password_entry.insert(0, password)

	copy(password)

	messagebox.showinfo(title='Password Copied', message='Generated Password is copied!!')

def save_password():
	if hash_password.get() == 1:
		password = hp.encrypt(password_entry.get())
	else:
		password = password_entry.get()

	website = website_entry.get().lower()
	email = email_entry.get()
	data_new = {
		website: {
			"email": email,
			"password": password
		}
	}

	if len(website) == 0 or len(email) == 0 or len(password) == 0:
		messagebox.showwarning(title="Oops!!", message='Please fill all the fields!!')
		return 

	try: 
		with open('passwords.json', 'r') as file:
			data = load(file)
	except FileNotFoundError:
		with open('passwords.json', 'w') as file:
			dump(data_new, file, indent=4)
	else:
		data.update(data_new)
		with open('passwords.json', 'w') as file:
			dump(data, file, indent=4)
	finally:
		msg = f'Password details saved successfully for {website.capitalize()}'
		title = 'Password Saved Successfully'
		messagebox.showinfo(title=title, message=msg)
		
	website_entry.delete(0, END)
	password_entry.delete(0, END)


win = Tk()
win.title('Password Manager')
win.config(padx=50, pady=20)

canvas = Canvas(width=200, height=200)
# logo = PhotoImage(file='logo.png')
logo = PhotoImage(file=os.path.join(os.getcwd(),"logo.png"))

canvas.create_image(100,100, image=logo)
canvas.grid(row=0, column=0, columnspan=3)

# Labels
website_label = Label(text='Website / URL: ', font=("Bell MT", 14))
website_label.grid(row=1, column=0, sticky ='E')
email_label = Label(text='Email / Username: ', font=("Bell MT", 14))
email_label.grid(row=2, column=0, sticky ='E')
password_label = Label(text='Password: ', font=("Bell MT", 14))
password_label.grid(row=3, column=0, sticky ='E')

# Entries
website_entry = Entry(width=25, font=("Bell MT", 14, 'bold'), borderwidth=4, relief=GROOVE, bd=1)
website_entry.grid(sticky='W', row=1, column=1, pady=8)
website_entry.focus()
email_entry = Entry(width=42, font=("Bell MT", 14, 'bold'), borderwidth=4, relief=GROOVE, bd=1)
email_entry.grid(sticky='W', row=2, column=1, columnspan=2, pady=8)
# email_entry.insert(0, 'raja@gmail.com')
password_entry = Entry(width=25, font=("Bell MT", 14, 'bold'), borderwidth=4, relief=GROOVE, bd=1)
password_entry.grid(sticky='W', row=3, column=1, pady=8, padx=(0, 10))

# Buttons
search_btn = Button(text='Search', width=15, height=1, font=("Bell MT", 12, 'bold'), command=search_password, relief=GROOVE, bd=2)
search_btn.grid(row=1, column=2)
generate_password_btn = Button(text='Generate Password', width=15, height=1, font=("Bell MT", 12, 'bold'), command=generate_password, relief=GROOVE, bd=2)
generate_password_btn.grid(row=3, column=2)

hash_password = IntVar()
hash_password_cb = Checkbutton(text="Hash Password", variable=hash_password, font=("Bell MT", 12, 'bold'), padx=15, pady=1, relief=GROOVE)
hash_password_cb.grid(row=4, column=1, sticky='N', pady=(8, 50))

add_btn = Button(text='A D D', width=15, font=("Bell MT", 12, 'bold'), command=save_password, relief=GROOVE, bd=2)
add_btn.grid(row=4, column=2, columnspan=1, pady=(8, 50))

win.mainloop()