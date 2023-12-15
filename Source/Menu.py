from tkinter import messagebox
from customtkinter import *
from PIL import Image
from new_message import new_message_widget
import json
import Receive_email
from move_folder import *

def coming_soon():
    messagebox.showinfo("Coming Soon", "This feature is coming soon!")

def new_message_window(app):
    root = CTkToplevel()
    app.withdraw()

    with open('config.json', 'r') as f:
        data = json.load(f)

    new_message_widget(root, data)

    # Set a function to be called when the window is closed
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, app))

    root.mainloop()


def on_close(root, app):
    root.destroy()  # Destroy the root window
    app.deiconify()  # Show the app window


def on_close(root, app):
    root.destroy()  # Destroy the root window
    app.deiconify()  # Show the app window

class Menu(CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        self.prev_button = None
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
        self.path = os.path.join(os.path.dirname(__file__), data["Usermail"])
        set_appearance_mode("dark")

        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure((1,2,3,4,5,6,7), weight=1, uniform='a')
        self.columnconfigure(0, weight=5, uniform='a')

        self.create_widgets()

    def create_widgets(self):    
        new_message_img = Image.open("assets\\new_message.png")
        self.download_and_new_message_frame = CTkFrame(self)
        self.download_and_new_message_frame.grid(row=0, column=0, sticky="nsew")

        download_img = Image.open("assets\\download.png").resize((20, 20))
        self.download_button = CTkButton(master=self.download_and_new_message_frame, text="", corner_radius=32,
                                         image=CTkImage(dark_image=download_img, light_image=download_img),
                                         width=15, height=15, command=self.download_email)
        self.download_button.pack(pady=10, side="top")

        self.new_message_button = CTkButton(master=self.download_and_new_message_frame, text="New Message", corner_radius=32, border_width=2,
                                       image=CTkImage(dark_image=new_message_img, light_image=new_message_img),
                                       width=70, height=50, fg_color="#4158D0", hover_color="#C850C0",
                                       border_color="#FFCC70", command=lambda: new_message_window(self.master))
        self.new_message_button.pack(padx=5, pady=10, side="left")

        # Create images
        inbox_image = Image.open("assets\\inbox.png")
        star_image = Image.open("assets\\star.png")
        sent_image = Image.open("assets\\sent.png")
        trash_image = Image.open("assets\\trash.png")
        spam_image = Image.open("assets\\spam.png")
        work_image = Image.open("assets\\work.png")

        # Create buttons
        self.inbox_button = CTkButton(master=self, text="Inbox", corner_radius=48, border_width=2, width=70, height=50,
                                          image=CTkImage(dark_image=inbox_image, light_image=inbox_image), fg_color="transparent",
                                          command=lambda text="Inbox": self.handle_command(text))
        self.star_button = CTkButton(master=self, text="Star", corner_radius=48, border_width=2, width=70, height=50,
                                      image=CTkImage(dark_image=star_image, light_image=star_image), fg_color="transparent",
                                      command=lambda text="Star": self.handle_command(text))
        self.sent_button = CTkButton(master=self, text="Sent", corner_radius=48, border_width=2, width=70, height=50,
                                      image=CTkImage(dark_image=sent_image, light_image=sent_image), fg_color="transparent",
                                      command=lambda text="Sent": self.handle_command(text))
        self.trash_button = CTkButton(master=self, text="Trash", corner_radius=48, border_width=2, width=70, height=50,
                                      image=CTkImage(dark_image=trash_image, light_image=trash_image), fg_color="transparent",
                                      command=lambda text="Trash": self.handle_command(text))
        self.spam_button = CTkButton(master=self, text="Spam", corner_radius=48, border_width=2, width=70, height=50,
                                      image=CTkImage(dark_image=spam_image, light_image=spam_image), fg_color="transparent",
                                      command=lambda text="Spam": self.handle_command(text))
        self.work_button = CTkButton(master=self, text="Work", corner_radius=48, border_width=2, width=70, height=50,
                                      image=CTkImage(dark_image=work_image, light_image=work_image), fg_color="transparent",
                                      command=lambda text="Work": self.handle_command(text))

        # Create grid
        self.inbox_button.grid(row=1, column=0, sticky="nsew")
        self.star_button.grid(row=2, column=0, sticky="nsew")
        self.sent_button.grid(row=3, column=0, sticky="nsew")
        self.trash_button.grid(row=4, column=0, sticky="nsew")
        self.spam_button.grid(row=5, column=0, sticky="nsew")
        self.work_button.grid(row=6, column=0, sticky="nsew")

    def handle_command(self, text):
        folder_name = os.path.join(self.path, text)
        # Check if the directory does not exist before trying to create it
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        if self.prev_button != None:
            self.prev_button.configure(fg_color="transparent")
        if text == "Inbox":
            print("Inbox","That's it")
            self.inbox_button.configure(fg_color="Mediumblue")
            self.prev_button = self.inbox_button
            self.callback("Inbox")
        elif text == "Star":
            print("Star")
            try:
                for folder in os.listdir(folder_name):
                    print(folder, "!!")
                    if os.path.isdir(os.path.join(folder_name, folder)):
                        folder_mail = os.path.join(folder_name, folder)
                        with open(os.path.join(folder_mail, "infor.json"), 'r') as file:
                            data = json.load(file)
                        if data["Star"] == str(False):
                            prev_folder = os.path.join(os.path.dirname(__file__), data["Pre_Folder"])
                            print(prev_folder)
                            delete_subfolder(prev_folder, folder)
                            move_subfolder(folder_name, prev_folder, folder)
            except Exception as e:
                print(e)

            self.star_button.configure(fg_color="Mediumblue")
            self.prev_button = self.star_button
            self.callback("Star")
        elif text == "Sent":
            print("Sent")
            self.sent_button.configure(fg_color="Mediumblue")
            self.prev_button = self.sent_button
            self.callback("Sent")
        elif text == "Trash":
            print("Trash")
            self.trash_button.configure(fg_color="Mediumblue")
            self.prev_button = self.trash_button
            self.callback("Trash")
        elif text == "Spam":
            print("Spam")
            self.spam_button.configure(fg_color="Mediumblue")
            self.prev_button = self.spam_button
            self.callback("Spam")
        elif text == "Work":
            print("Work")
            self.work_button.configure(fg_color="Mediumblue")
            self.prev_button = self.work_button
            self.callback("Work")
        else:
            pass
            
    def download_email(self):
        try:
            with open('config.json', 'r') as f:
                data = json.load(f)

            Receive_email.get_email(data["Usermail"], data["PASS"], data["MailServer"], int(data["POP3"]))
        except Exception as e:
            print(e)