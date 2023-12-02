from logging import RootLogger
from tkinter import *
from tkinter import messagebox
import ast


root=Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

window_exists = BooleanVar()
window_exists.set(False)

def window_after_sign_in():
    screen = Toplevel(root)
    screen.title("App")
    screen.geometry('925x500+300+200')
    screen.config(bg='white')

    Label(screen, text='Hello every one', bg='#fff',font=('Calibri(Body)', 50,'bold')).pack(expand=True)

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

    # print(r.keys())
    # print(r.values())


    if username in r.keys() and password==r[username]:
        root.withdraw()
        window_after_sign_in()

    # elif username!='admin' and password!='1234':
    #     messagebox.showerror("Invalid","Invalid username and password !")
    
    # elif username!='admin':
    #     messagebox.showerror("Invalid","Invalid username!")

    # elif password!='1234':
    #     messagebox.showerror("Invalid","Invalid password!")           

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
                file.seek(0)  # Move the cursor to the beginning of the file
                file.truncate()  # Truncate the file content
                file.write(str(r))
                file.close()

                messagebox.showinfo('Signup', 'Successfully sign up')

                # Đóng cửa sổ đăng ký và hiển thị cửa sổ đăng nhập
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