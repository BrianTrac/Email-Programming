from customtkinter import *
from ctk_listbox import *
from content_frame import *
from move_folder import *
import json
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
        self.tool_bar = CTkFrame(self, fg_color="transparent")
        self.tool_bar.grid(row=0, sticky="nsew")
        self.tool_bar.back = False

        for i in range(18):
            self.tool_bar.grid_columnconfigure(i, weight=1)

        # Create images 
        back_image = Image.open("white_back_image.png").resize((20,20))
        spam_image = Image.open("white_spam_image.png").resize((20,20))
        trash_image = Image.open("white_trash_image.png").resize((20,20))
        move_folder_image = Image.open("white_move_folder_image.png").resize((20,20))

        # Create buttons
        self.tool_bar.back_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                              image=CTkImage(dark_image=back_image, light_image=back_image, size=(20, 20)), width=20,
                                              command= lambda text = "Back": self.handle_command(text))
        
        self.tool_bar.spam_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                              image=CTkImage(dark_image=spam_image, light_image=spam_image, size=(20, 20)), width=20,
                                              command= lambda text = "Spam": self.handle_command(text))
        
        self.tool_bar.trash_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                              image=CTkImage(dark_image=trash_image, light_image=trash_image, size=(20, 20)), width=20,
                                              command= lambda text = "Trash": self.handle_command(text))
           
        self.tool_bar.move_folder_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                              image=CTkImage(dark_image=move_folder_image, light_image=move_folder_image, size=(20, 20)), width=20,
                                              command= lambda text = "Move": self.handle_command(text))

        if self.tool_bar.back:
            self.tool_bar.back_button.grid(row=0, column=0, sticky="nsew")
        
        self.tool_bar.spam_button.grid(row=0, column= 1, sticky="nsew")
        self.tool_bar.trash_button.grid(row=0, column=2, sticky="nsew")
        self.tool_bar.move_folder_button.grid(row=0, column=3, sticky="nsew")

    def create_scrollable_box(self):
        self.listbox = CTkListbox(self)
        self.listbox.grid(row=1, sticky="nsew")
        self.listbox.selected_button = None
        
    def update_main_frame(self, message):     
        if message != self.listbox.selected_button:
            path = "D:/Python/Socket Programming/Email"
            path = os.path.join(path, message)
            folder_list = sorted([folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))], key=int)
            size = len(folder_list)
            self.listbox.selected_button = message
            self.destroy_elements()


            for folder in folder_list:
                folder_name = os.path.basename(folder)
                folder = os.path.join(path, folder)
                with open(os.path.join(folder, str(folder_name) + ".json"), "r") as file:
                    data = json.load(file)
                    self.listbox.insert(int(size), data["From"].split(' ')[0], data["Subject"], data["Date"])
                    size = size - 1
        
    def destroy_elements(self):
        # Destroy all elements within the frame
        for widget in self.listbox.winfo_children():
            #if isinstance(widget, ContentFrame):
            widget.destroy()

    def handle_command(self, text):
        if text == "Back":
            print("Back")
        elif text == "Spam":
            print("Spam")
        elif text == "Trash":
            print("Trash")
        elif text == "Move":
            self.create_combobox()
            print("Move")
        else:
            pass
    
    def create_combobox(self):
        self.tool_bar.combobox = CTkOptionMenu(self.tool_bar, width=10)
        self.tool_bar.combobox.bind("<FocusOut>", self.hide_menu)
        self.tool_bar.combobox.bind("<Button-1>", self.show_menu)

    def hide_menu(self, event):
        self.tool_bar.combobox.place_forget()
    
    def show_menu(self, event):
        self.tool_bar.combobox['value'] = ["Spam", "Trash", "Important", "Work"]
        self.tool_bar.combobox.place(x=300, y=200)