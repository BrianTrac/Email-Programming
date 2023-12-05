def signup(username_entry, password_entry, confirm_password_entry, window):
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    try:
        # Read existing user data
        file = open('datasheet.txt', 'r+')
        data = file.read()
        users_data = ast.literal_eval(data)
    except FileNotFoundError:
        # If the file doesn't exist, create it with default data
        file = open('datasheet.txt', 'w')
        default_data = str({'Username': 'password'})
        file.write(default_data)
        file.close()
        users_data = {'Username': 'password'}

    if username in users_data:
        messagebox.showerror('Invalid', 'Username already exists')
        self.reset_signin_fields()
    elif password == confirm_password:
        # Update user data with the new user
        users_data[username] = password

        file.seek(0)
        file.truncate()
        file.write(str(users_data))
        file.close()

        messagebox.showinfo('Signup', 'Successfully signed up')
        self.reset_signin_fields()
        window.destroy()
        self.root.deiconify()
        self.window_exists.set(False)
    else:
        messagebox.showerror('Invalid', "The passwords don't match ")
        self.reset_signin_fields()
