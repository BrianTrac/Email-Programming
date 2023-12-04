from logging import RootLogger
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Tk, Toplevel, Frame, Label, StringVar, PhotoImage
import ast
root=Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

window_exists = BooleanVar()
window_exists.set(False)
    

def show_new_window():
    new_window = Toplevel(root)
    new_window.title("Send email")
    new_window.geometry('1000x720+400+35')
    new_window.config(bg='#121212')
    dark_mode = True
    if dark_mode:
        new_window.config(bg='#121212')
        text_color = 'white'
    else:
        new_window.config(bg='white')
        text_color = 'black'

    # Labels for "From" and "To"
    from_label = Label(new_window, text="From:", fg='white', bg=new_window.cget('bg'),
                       font=('Microsoft Yahei UI Light', 14))
    from_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    to_label = Label(new_window, text="To:", fg='white', bg=new_window.cget('bg'),
                     font=('Microsoft Yahei UI Light', 14))
    to_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    # Entry boxes for "From" and "To"
    from_entry = Entry(new_window, width=50, font=('Segoe UI', 12), bg ='#2F3138', fg = 'white')
    from_entry.grid(row=0, column=1, padx=10, pady=10)

    to_entry = Entry(new_window, width=50, font=('Segoe UI', 12), bg ='#2F3138', fg='white')
    to_entry.grid(row=1, column=1, padx=10, pady=10)

    # Button to send the email (you can customize this)
    send_button = Button(new_window, text="Send", command=send_email, bg='#4CAF50', fg='white',
                         font=('Microsoft Yahei UI Light', 14))
    send_button.grid(row=2, column=1, pady=20)

def send_email():
    # Implement the logic to send the email here
    pass


def show_email_window():
    open_email_window = Toplevel(root)
    open_email_window.title("Open Email Window")
    open_email_window.geometry('1280x720+110+35')
    open_email_window.config(bg='#2E2E2E')
    dark_mode = True
    if dark_mode:
        open_email_window.config(bg='#2E2E2E')
        text_color = 'white'
    else:
        open_email_window.config(bg='white')
        text_color = 'black'

# Text
def on_text_click(event):
    new_email_window = Toplevel(root)
    new_email_window.title("New Email")
    new_email_window.geometry('400x200+300+150')


# Inbox
def on_inbox_message_enter(event):
    small_frame.config(bg='#B3E0FF')  # Set the background color when the cursor enters
    inbox_message.config(bg='#B3E0FF')  # Synchronize background color
    inbox_icon_label.config(bg='#B3E0FF')  # Synchronize background color

def on_inbox_label_click(event):
    new_email_window = Toplevel(root)
    new_email_window.title("New Email")
    new_email_window.geometry('400x200+300+150')

def on_small_frame_enter(event):
    small_frame.config(bg='#B3E0FF')  # Set the background color when the cursor enters
    inbox_message.config(bg='#B3E0FF')  # Synchronize background color
    inbox_icon_label.config(bg='#B3E0FF')  # Synchronize background color

def on_small_frame_leave(event):
    small_frame.config(bg='#EDE7FF')  # Set the background color when the cursor leaves
    inbox_message.config(bg='#EDE7FF')  # Synchronize background color
    inbox_icon_label.config(bg='#EDE7FF')  # Synchronize background color


# email sent
def on_sent_label_click(event):
    new_email_window = Toplevel(root)
    new_email_window.title("New Email")
    new_email_window.geometry('400x200+300+150')

def on_star_label_click(event):
    new_email_window = Toplevel(root)
    new_email_window.title("New Email")
    new_email_window.geometry('400x200+300+150')

def on_trash_label_click(event):
    new_email_window = Toplevel(root)
    new_email_window.title("New Email")
    new_email_window.geometry('400x200+300+150')


# Sample Data
data = [
    ["Shopee", "Sieu Sale 12/12", "7:00AM 4/12/2023"],
    ["Github", "Verify Email Address", "6:00PM 3/12/2023"],
    # Add more rows as needed
]
def window_after_sign_in():
    screen = Toplevel(root)
    screen.title("App")
    screen.geometry('1280x720+110+35')
    screen.config = 'white'

    frame = Frame(screen, width=250, height=800, bg = '#EDE7FF')
    frame.place(x=0, y=0)

    text_content = StringVar()
    text_content.set(" +    New Email    ")    

    global text_box
    text_box = Label(frame, textvariable=text_content, font=("Segoe UI", 18, "bold"), fg="white", bg = '#7AD4F0',cursor="hand2")
    text_box.place(x=10, y=15)   

    text_box.bind("<Button-1>", on_text_click)
    # Inbox

    # Create the small frame
    global small_frame
    small_frame = Frame(frame, width=250, height=40, bg='#EDE7FF')
    small_frame.place(x=0, y=85)  # Adjust the y-coordinate to avoid overlapping
    
    global inbox_message
    inbox_message = Label(frame, text="Inbox", fg='black', bg='#EDE7FF', font=('Segoe UI', 14), cursor='hand2')
    inbox_message.place(x=80, y=85)
    inbox_message.bind("<Enter>", on_inbox_message_enter)

    global inbox_icon_label
    inbox_icon = PhotoImage(file='inbox_icon.png').subsample(2, 2)
    inbox_icon_label = Label(frame, image=inbox_icon, bg='#EDE7FF')
    inbox_icon_label.image = inbox_icon
    inbox_icon_label.place(x=30, y=87)

    small_frame.bind("<Enter>", on_small_frame_enter)
    small_frame.bind("<Leave>", on_small_frame_leave)


    inbox_message.bind("<Button-1>", on_inbox_label_click)


    # Email Sent
    sent_message = Label(frame, text = "Email Sent", fg='black', bg = '#EDE7FF', font=('Segoe UI', 14), cursor='hand2')
    sent_message.place(x=80,y=155)

    sent_icon = PhotoImage(file='sent_icon.png').subsample(2,2)
    sent_icon_label = Label(frame, image = sent_icon, bg='#EDE7FF')
    sent_icon_label.image = sent_icon
    sent_icon_label.place(x = 30, y = 157)

    sent_message.bind("<Button-1>", on_sent_label_click)   

    # Star
    star_message = Label(frame, text = "Important Email", fg='black', bg = '#EDE7FF', font=('Segoe UI', 14), cursor='hand2')
    star_message.place(x=80,y=225)

    star_icon = PhotoImage(file='star_icon.png').subsample(2,2)
    star_icon_label = Label(frame, image = star_icon, bg='#EDE7FF')
    star_icon_label.image = star_icon
    star_icon_label.place(x = 30, y = 225)

    star_message.bind("<Button-1>", on_star_label_click)      

    # Trash
    trash_message = Label(frame, text = "Trash", fg='black', bg = '#EDE7FF', font=('Segoe UI', 14), cursor='hand2')
    trash_message.place(x=80,y=295)

    trash_icon = PhotoImage(file='trash_icon.png').subsample(2,2)
    trash_icon_label = Label(frame, image = trash_icon, bg='#EDE7FF')
    trash_icon_label.image = trash_icon
    trash_icon_label.place(x = 30, y = 295)

    trash_message.bind("<Button-1>", on_trash_label_click)      

    # Table Frame
    table_frame = Frame(screen, width=1200, height=650, bg='white')
    table_frame.place(x=300, y=100)

    # Headers
    headers = ["Sender", "Content", "Date"]
    column_widths = [max(len(header), max(len(str(row_data[col])) for row_data in data)) for col, header in enumerate(headers)]

    for col, header in enumerate(headers):
        label = Label(table_frame, text=header, font=('Segoe UI', 14, 'bold'), bg='#EDE7FF', padx=120, pady=7,
                      borderwidth=1, relief='solid', width=column_widths[col])
        label.grid(row=0, column=col)

    # Populate the table
    for row, row_data in enumerate(data, start=1):
        for col, value in enumerate(row_data):
            label = Label(table_frame, text=value, font=('Segoe UI', 14), bg='#EDE7FF', padx=120, pady=7, borderwidth=1,
                          relief='solid', width=column_widths[col])
            label.grid(row=row, column=col)


    screen.protocol("WM_DELETE_WINDOW", lambda: show_login_window(screen))


def show_login_window(screen):
    screen.destroy()
    root.deiconify()


def signin():
    username=user.get()
    password=code.get()
    

    file=open('datasheet.txt','r')

    d=file.read()
    r=ast.literal_eval(d)
    file.close()



    if username in r.keys() and password==r[username]:
        root.withdraw()
        window_after_sign_in()      

    else:
        messagebox.showerror('Invalid','invalid username or password')    




######@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def signup_command():
    window=Toplevel(root)
    window.title("SignUp")
    window.geometry('925x500+300+200')
    window.configure(bg='#fff')
    window.resizable(False, False)

    def signup():
        username = user.get()
        password = code.get()
        confirm_password = confirm_code.get()

        if password == confirm_password:
            try:
                file = open('datasheet.txt', 'r+')
                d = file.read()
                r = ast.literal_eval(d)

                dict2 = {username: password}
                r.update(dict2)
                file.seek(0) 
                file.truncate()  
                file.write(str(r))
                file.close()

                messagebox.showinfo('Signup', 'Successfully sign up')

                window.destroy()
                root.deiconify()
                window_exists.set(False)                
            except:
                file=open('datasheet.txt','w')
                pp=str({'Username':'password'})
                file.write(pp)
                file.close()
        else:
            messagebox.showerror('Invalid', "The passwords don't match ")
            window.destroy()

    def sign():
        window.destroy()

    img = PhotoImage(file='signup.png')
    Label(window,image=img,border=0,bg='white').place(x=50,y=90)

    frame = Frame(window,width=350,height=390,bg='#fff')

    frame.place(x=480,y=50)


    heading=Label(frame,text='Sign up', fg='#57a1f8',bg='white',font=('Microsoft Yahei UI Light', 23,'bold'))
    heading.place(x=100,y=5)

######---------------------------------------

    def on_enter(e):
        user.delete(0,'end')
    def on_leave(e):
        if user.get()=='':
          user.insert(0,'Username')

    user = Entry(frame,widt=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light', 11))
    user.place(x=30,y=80)
    user.insert(0,'Username')
    user.bind("<FocusIn>", on_enter)
    user.bind("<FocusOut>", on_leave)


    Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)



######-------------------------------------------


    def on_enter(e):
      code.delete(0,'end')
    def on_leave(e):
        if code.get()=='':
            code.insert(0,'Password')

    code = Entry(frame,widt=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light', 11))
    code.place(x=30,y=150)
    code.insert(0,'Password')
    code.bind('<FocusIn>', on_enter)
    code.bind('<FocusOut>', on_leave)


    Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)


######-------------------------------------------

    def on_enter(e):
        confirm_code.delete(0,'end')
    def on_leave(e):
        if confirm_code.get()=='':
            confirm_code.insert(0,'Confirm Password')

    confirm_code = Entry(frame,widt=25,fg='black',border=0,bg='white',font=('Microsoft Yahei UI Light', 11))
    confirm_code.place(x=30,y=220)
    confirm_code.insert(0,'Confirm Password')
    confirm_code.bind('<FocusIn>', on_enter)
    confirm_code.bind('<FocusOut>', on_leave)


    Frame(frame,width=295,height=2,bg='black').place(x=25,y=247)



####----------------------------------------

    Button(frame,width=39,pady=7,text='Sign up', bg='#57a1f8',fg='white',border=0,command=signup).place(x=35,y=280)
    label=Label(frame,text='I have an account',fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
    label.place(x=90,y=340)

    signin =Button(frame,width=6,text='Sign in', border = 0, bg='white', cursor='hand2',fg='#57a1f8',command=sign)
    signin.place(x=200,y=340)
    if not window_exists.get():
        window_exists.set(True)




    window.mainloop()    
######@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

img = PhotoImage(file='login.png')
Label(root,image=img,bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading=Label(frame, text='Sign in', fg="#57a1f8", bg = "white", font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100,y=5)

#########------------------------------------------

def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

user = Entry(frame, width=25, fg='black',border=0, bg="white",font=('Microsoft YaHei UI Light', 11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295,height=2,bg='black').place(x=25,y=107)

#########-------------------------------------------

def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')

code = Entry(frame, width=25, fg='black',border=0, bg="white",font=('Microsoft YaHei UI Light', 11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295,height=2,bg='black').place(x=25,y=177)

####################################################

Button(frame,width=39,pady=7,text='Sign in', bg="#57a1f8",fg='white',border=0,command=signin).place(x=35,y=204)
label=Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Microsoft YaHei UI Light', 9))
label.place(x=75,y=270)

sign_up=Button(frame,width=6,text='Sign up', border=0,bg='white',cursor='hand2',fg='#57a1f8',command=signup_command)
sign_up.place(x=215,y=270)





root.mainloop()