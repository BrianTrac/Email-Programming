from customtkinter import *
from PIL import Image

class Main(CTkFrame):
    def __init__(self, master):
        super().__init__(master) 

        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=15, uniform='a')
        self.columnconfigure(0, weight=5, uniform='a')

        self.create_widgets()

    def create_widgets(self):
        self.create_tool_bar()
        self.create_scrollable_box()

    def create_tool_bar(self):
        tool_bar = CTkFrame(self, fg_color="Snow1")
        tool_bar.grid(row=0, sticky="nsew")

        tool_buttons = [
            ("Back", "back_image.png"), ("Spam", "spam_image_4.png"),
            ("Trash", "trash_image.png"), ("Read", "read_image.png"),
            ("Unread", "unread_image.png"), ("Move", "move_folder_image.png")        
        ]

        for i in range(3*len(tool_buttons)):
            tool_bar.grid_columnconfigure(i, weight=1)

        for i, (text, image) in enumerate(tool_buttons):
            print(i)
            image = Image.open(f"{image}")
            button = CTkButton(master=tool_bar, text = "", corner_radius=20, fg_color="Snow1", hover_color="Snow2", width=20, 
                               image=CTkImage(dark_image=image, light_image=image, size=(20, 20)),  command=self.handle_command)
            button.grid(row=0, column=i, sticky="nsew")

    def create_scrollable_box(self):
        scrollable_frame = CTkFrame(self, fg_color="Snow3").grid(row=1, sticky="nsew")

    def handle_command(self):
        print("command")
    