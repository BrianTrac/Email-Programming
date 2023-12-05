from tkinter import BooleanVar, Tk, Toplevel, Frame, Label, Entry, Button, PhotoImage, messagebox
import ast
import customtkinter
class LoginApp:
    def __init__(self):
        # Initialize the main application window
        self.root = Tk()
        self.root.title('Login')
        self.root.geometry('925x500+300+200')
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)

        # Variable to track the existence of the sign-up window
        self.window_exists = BooleanVar(None)
        self.window_exists.set(False)

        # Set up the main login window
        self.setup_login_window()

    def setup_login_window(self):
        # Set up the main login window interface
        img = PhotoImage(file='login.png')
        Label(self.root, image=img, bg='white').place(x=50, y=50)

        frame = Frame(self.root, width=350, height=350, bg="white")
        frame.place(x=480, y=70)

        heading = Label(frame, text='Sign in', fg="#57a1f8", bg="white", font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        # Entry widgets for username and password
        self.username_entry = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.username_entry.place(x=30, y=80)
        self.handle_entry(self.username_entry, 'Username')

        self.password_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.password_entry.place(x=30, y=150)
        self.handle_entry(self.password_entry, 'Password', show_password=True)
        self.create_eye_button(frame, 322, 157, self.password_entry)

        # Separators and Sign In button
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)
        Button(frame, width=39, pady=7, text='Sign in', bg="#57a1f8", fg='white', border=0,
               command=self.signin).place(x=35, y=204)

        # "Don't have an account?" label and Sign Up button
        label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
        label.place(x=75, y=270)

        sign_up_button = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8',
                                command=self.signup_command)
        sign_up_button.place(x=215, y=270)

        # Start the main application event loop
        self.root.mainloop()

    def handle_entry(self, entry, default_text, show_password=False):
        # Functions to handle entry widget focus events (on_enter and on_leave)
        def on_enter(e):
            if entry.get() == default_text:
                entry.delete(0, 'end')
                if show_password:
                    entry.config(show='*')

        def on_leave(e):
            if entry.get() == '':
                entry.insert(0, default_text)
                if show_password:
                    entry.config(show='')

        # Set default text and bind focus events
        entry.insert(0, default_text)
        entry.bind('<FocusIn>', on_enter)
        entry.bind('<FocusOut>', on_leave)

    def create_eye_button(self, frame, place_x, place_y, password_entry):
        # Function to create an eye button for showing/hiding password
        eye_icon = PhotoImage(file='eye_icon.png').subsample(2, 2)
        eye_button = Button(frame, image=eye_icon, bg='white', borderwidth=0)
        eye_button.image = eye_icon  # Store the image reference
        eye_button.place(x=place_x, y=place_y)

        def start_showing_password(event):
            password_entry.config(show='')

        def stop_showing_password(event):
            password_entry.config(show='*')

        # Bind mouse events to show/hide password
        eye_button.bind("<ButtonPress-1>", start_showing_password)
        eye_button.bind("<ButtonRelease-1>", stop_showing_password)

    def reset_signin_fields(self):
        # Function to reset the username and password entry fields(reset thanh cac o trong)
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.handle_entry(self.username_entry, 'Username')
        self.handle_entry(self.password_entry, 'Password', show_password=True)

    def signin(self):
        # Functionality for signing in
        username = self.username_entry.get()
        password = self.password_entry.get()

        file = open('datasheet.txt', 'r')
        data = file.read()
        users_data = ast.literal_eval(data)
        file.close()

        if username in users_data.keys() and password == users_data[username]:
            self.root.withdraw()
            self.window_after_sign_in()
        else:
            messagebox.showerror('Invalid', 'Invalid username or password')

    def signup_command(self):
        # Functionality for handling Sign Up button click
        if not self.window_exists.get():
            self.window_exists.set(True)

        self.root.withdraw()    # Hide main login

        window = Toplevel(self.root)
        window.title("SignUp")
        window.geometry('925x500+300+200')
        window.configure(bg='#fff')
        window.resizable(False, False)


        # Function to handle Sign Up process
        def signup(username_entry, password_entry, confirm_password_entry, window):
            username = username_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            if password == confirm_password:
                try:
                    file = open('datasheet.txt', 'r+')
                    data = file.read()
                    users_data = ast.literal_eval(data)

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
                except:
                    file = open('datasheet.txt', 'w')
                    default_data = str({'Username': 'password'})
                    file.write(default_data)
                    file.close()
            else:
                messagebox.showerror('Invalid', "The passwords don't match ")
                self.reset_signin_fields()

        def sign(window):
            # Function to handle closing the Sign Up window(if close Sign up window, return main login window)
            window.destroy()
            self.reset_signin_fields()

            self.root.deiconify()   # Show again

        # Interface of sign up window
        img = PhotoImage(file='signup.png')
        Label(window, image=img, border=0, bg='white').place(x=50, y=90)

        frame = Frame(window, width=350, height=390, bg='#fff')
        frame.place(x=480, y=50)

        heading = Label(frame, text='Sign up', fg='#57a1f8', bg='white', font=('Microsoft Yahei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        # Entry widgets for Sign Up window
        user_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        user_entry.place(x=30, y=80)
        self.handle_entry(user_entry, 'Username')

        code_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        code_entry.place(x=30, y=150)
        self.handle_entry(code_entry, 'Password', show_password=True)
        self.create_eye_button(frame, 322, 160, code_entry)

        confirm_code_entry = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        confirm_code_entry.place(x=30, y=220)
        self.handle_entry(confirm_code_entry, 'Confirm Password', show_password=True)
        self.create_eye_button(frame, 322, 230, confirm_code_entry)

        # Separators and Sign Up button
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)
        Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

        Button(frame, width=39, pady=7, text='Sign up', bg='#57a1f8', fg='white', border=0,
               command=lambda: signup(user_entry, code_entry, confirm_code_entry, window)).place(x=35, y=280)
        label = Label(frame, text='I have an account', fg='black', bg='white',
                      font=('Microsoft YaHei UI Light', 9))
        label.place(x=90, y=340)

        signin_button = Button(frame, width=6, text='Sign in', border=0, bg='white', cursor='hand2', fg='#57a1f8',
                               command=lambda: sign(window))
        signin_button.place(x=200, y=340)
        window.protocol("WM_DELETE_WINDOW", lambda: sign(window))
        window.mainloop()      

    def window_after_sign_in(self):
        # Functionality for creating the main application window after sign in
        screen = Toplevel(self.root)
        screen.title("App")
        screen.geometry('1280x720+110+35')
        screen.config(bg='white')

        # Set up closing behavior for the sign-in window
        screen.protocol("WM_DELETE_WINDOW", lambda: self.show_login_window(screen))

    def show_login_window(self, screen):
        # Functionality for showing the login window after closing the main application window
        screen.destroy()
        self.root.deiconify()
        self.reset_signin_fields()

# Run the application if this script is executed
if __name__ == "__main__":
    app = LoginApp()
