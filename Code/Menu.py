from tkinter import messagebox
from customtkinter import *
from PIL import Image
from new_message import new_message_widget

def new_message_window(app):
    root = CTkToplevel()
    app.withdraw()
    new_message_widget(root, "Peter", "peter113@gmail.com")

    # Set a function to be called when the window is closed
    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root, app))

    root.mainloop()


def on_close(root, app):
    root.destroy()  # Destroy the root window
    app.deiconify()  # Show the app window

class Menu(CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
        set_appearance_mode("dark")

        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure((1,2,3,4,5,6,7), weight=1, uniform='a')
        self.columnconfigure(0, weight=5, uniform='a')

        self.create_widgets()

    def create_widgets(self):
    
        new_message_img = Image.open("new_message.png")
        self.new_message_button = CTkButton(master=self, text="New Message", corner_radius=32, border_width=2,
                                       image=CTkImage(dark_image=new_message_img, light_image=new_message_img),
                                       width=150, height=70, fg_color="#4158D0", hover_color="#C850C0",
                                       border_color="#FFCC70", command=lambda: new_message_window(self.master))
        self.new_message_button.grid(row=0, column=0, padx=15, pady=10)

        button_info = [
            # {"text": "New Message", "image_path": "new_message.png", "width": 150, "height": 60},
            {"text": "Inbox", "image_path": "inbox.png", "width": 70, "height": 50},
            {"text": "Star", "image_path": "star.png", "width": 70, "height": 50},
            {"text": "Sent", "image_path": "sent.png", "width": 70, "height": 50},
            {"text": "Trash", "image_path": "trash.png", "width": 70, "height": 50},
            {"text": "Spam", "image_path": "spam.png", "width": 70, "height": 50},
        ]

        
        for row_index, button_data in enumerate(button_info):
            img = Image.open(button_data["image_path"])
            button = CTkButton(master=self, text=button_data["text"], corner_radius=48, border_width=2,
                               image=CTkImage(dark_image=img, light_image=img), fg_color="transparent",
                               width=button_data["width"], height=button_data["height"], command= lambda text=button_data["text"]: self.handle_command(text))
            button.grid(row=row_index + 1, column=0, sticky="nsew")
            

    def handle_command(self, text):
        if text == "Inbox":
            print("Inbox")
            self.callback("Inbox")
        elif text == "Star":
            print("Star")
            self.callback("Star")
        elif text == "Sent":
            print("Sent")
            self.callback("Sent")
        elif text == "Trash":
            print("Trash")
            self.callback("Trash")
        elif text == "Spam":
            print("Spam")
            self.callback("Spam")
        else:
            pass
            
