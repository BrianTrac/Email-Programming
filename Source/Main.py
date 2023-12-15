from customtkinter import *
from ctk_listbox import *
from content_frame import *
from move_folder import *
import json
import os
from PIL import Image
from show_receive_email_frame import *

path = os.path.dirname(__file__)
json_path = os.path.join(path, "config.json")

with open(json_path) as json_file:
    data = json.load(json_file)
    Usermail = data['Usermail']


class Main(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create Folder
        self.user_folder = os.path.join(os.path.dirname(__file__), Usermail)
        if not os.path.exists(self.user_folder):
            os.makedirs(self.user_folder)
        self.trash_folder = os.path.join(self.user_folder, "Trash")
        self.spam_folder = os.path.join(self.user_folder, "Spam")
        self.star_folder = os.path.join(self.user_folder, "Star")
        self.inbox_folder = os.path.join(self.user_folder, "Inbox")

        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=15, uniform='a')
        self.columnconfigure(0, weight=5, uniform='a')

        self.create_widgets()

    def create_widgets(self):
        self.create_tool_bar()
        self.create_scrollable_box()

    def create_tool_bar(self):
        self.combobox = None # use to create combobox for move function
        self.move_to = None # use for move function
        self.tool_bar = CTkFrame(self, fg_color="transparent")
        self.tool_bar.grid(row=0, sticky="nsew")
        self.move_selected = False

        for i in range(18):
            self.tool_bar.grid_columnconfigure(i, weight=1)

        # Create images
        back_image = Image.open("assets\\white_back_image.png").resize((20, 20))
        spam_image = Image.open("assets\\white_spam_image.png").resize((20, 20))
        trash_image = Image.open("assets\\white_trash_image.png").resize((20, 20))
        move_folder_image = Image.open("assets\\white_move_folder_image.png").resize((20, 20))

        # Create buttons
        self.tool_bar.back_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                              image=CTkImage(dark_image=back_image, light_image=back_image, size=(20, 20)), width=20,
                                              command=lambda text="Back": self.handle_command(text))

        self.tool_bar.spam_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                              image=CTkImage(dark_image=spam_image, light_image=spam_image, size=(20, 20)), width=20,
                                              command=lambda text="Spam": self.handle_command(text))

        self.tool_bar.trash_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                               image=CTkImage(dark_image=trash_image, light_image=trash_image, size=(20, 20)), width=20,
                                               command=lambda text="Trash": self.handle_command(text))

        self.tool_bar.move_folder_button = CTkButton(master=self.tool_bar, text="", corner_radius=20, fg_color="transparent", hover_color="Gray31",
                                                     image=CTkImage(dark_image=move_folder_image, light_image=move_folder_image, size=(20, 20)), width=20,
                                                     command=lambda text="Move": self.handle_command(text))

        self.tool_bar.back_button.grid(row=0, column=0, sticky="nsew")
        self.tool_bar.back_button.grid_remove()
        self.tool_bar.spam_button.grid(row=0, column=1, sticky="nsew")
        self.tool_bar.trash_button.grid(row=0, column=2, sticky="nsew")
        self.tool_bar.move_folder_button.grid(row=0, column=3, sticky="nsew")

    def create_scrollable_box(self):
        self.listbox = CTkListbox(self, callback=self.update_content_frame)
        self.listbox.grid(row=1, sticky="nsew")
        self.listbox.selected_button = None

    def update_main_frame(self, message):
        self.message = message
        if self.message != self.listbox.selected_button:
            self.path = os.path.join(os.path.dirname(__file__), Usermail)
            self.path = os.path.join(self.path, self.message)
            self.folder_list = sorted([folder for folder in os.listdir(
                self.path) if os.path.isdir(os.path.join(self.path, folder))], key=int, reverse=True)
            self.listbox.selected_button = message
            self.destroy_elements()

            batch = 0
            max_batch = len(self.folder_list)
            if self.message != "Sent":
                for folder in self.folder_list:
                    folder_name = folder
                    print(int(folder_name))
                    folder = os.path.join(self.path, folder)
                    with open(os.path.join(folder, "infor.json"), "r") as file:
                        data = json.load(file)

                        self.listbox.insert(int(folder_name), data["From"][:data["From"].find('<')].strip(), data["Subject"], data["Date"], folder)
                        batch = batch + 1
                        if batch == max_batch:
                            self.listbox.update()
                            batch = 0
            else:
                for folder in self.folder_list:
                    folder_name = folder
                    folder = os.path.join(self.path, folder)
                    with open(os.path.join(folder, "infor.json"), "r") as file:
                        data = json.load(file)
                        to = ""
                        try:
                            if len(data["To"]) == 1:
                                to = data["To"][0]
                            elif len(data["To"]) > 1:
                                to = data["To"][0] + " .."
                        except Exception as e:
                            print(e)
                            
                        self.listbox.insert(int(folder_name), to, data["Subject"], data["Date"], folder)
                        batch = batch + 1
                        if batch == max_batch:
                            self.listbox.update()
                            batch = 0

    def update_main_search_frame(self, To, From, Subject, Key):
        user_path = os.path.join(os.path.dirname(__file__), Usermail)
        for dir in ["Inbox", "Sent", "Spam", "Star", "Trash", "Work"]:
            path = os.path.join(user_path, dir)
            folder_list = sorted([folder for folder in os.listdir(
                path) if os.path.isdir(os.path.join(path, folder))], key=int, reverse=True)
            if dir == "Inbox":
                self.destroy_elements()

            for folder in folder_list:
                folder_name = folder
                folder = os.path.join(path, folder)
                print(folder)

                with open(os.path.join(folder, "infor.json"), "r") as file:
                    data = json.load(file)
                with open(os.path.join(folder, "content.txt"), "r") as file:
                    content = file.read()

                if self.check(data, To, From, Subject, Key, content):
                    print("OK", folder_name)
                    print(folder, "!!!")
                    self.listbox.insert(int(folder_name), "From: " + data["From"], data["Subject"], data["Date"], folder)


    def check(self, data, To, From, Subject, Key, content):
        if To != "" and To.lower() not in [data["To"][i].lower() for i in range(len(data["To"]))]:
            return False
        if From != "" and From.lower() not in data["From"].lower():
            return False
        if Subject != "" and Subject.lower() not in data["Subject"].lower():
            return False
        if Key != "" and Key not in content:
            return False
        return True

    def destroy_elements(self):
        # Destroy all elements within the frame
        for widget in self.listbox.winfo_children():
            # if isinstance(widget, ContentFrame):
            widget.destroy()

    def handle_command(self, text):
        try:
            if text == "Back":
                print("Back")
                self.tool_bar.back_button.grid_remove()
                self.show_email_content.destroy_window()
                for widget in self.listbox.winfo_children():
                    self.show_widget(widget)
            elif text == "Spam":
                self.clicked_handle("Spam")
                print("Spam")
            elif text == "Trash":
                self.clicked_handle("Trash")
                print("Trash")
            elif text == "Move":
                if self.move_selected:
                    self.move_selected = False
                    self.combobox.destroy()
                    self.combobox = None
                else:
                    self.move_selected = True
                    if self.combobox != None:
                        self.combobox.destroy()
                    self.create_combobox()
                print("Move")
            else:
                pass
        except Exception as e:
            print(e)

    def clicked_handle(self, text):
        folder_list = self.folder_list
        for folder in folder_list:
            if folder == None:
                continue
            folder_name = folder
            print(folder_name)
            folder = os.path.join(self.path, folder)
            try:
                with open(os.path.join(folder, "infor.json"), "r") as file:
                    data = json.load(file)
            except Exception as e:
                print(e)

            try:
                if data["Clicked"] == str(True):
                    if text == "Trash" and self.path != self.trash_folder and self.path != self.star_folder:
                        self.listbox.buttons[int(folder_name)].destroy()
                        self.listbox.update()
                        move_subfolder(self.path, self.trash_folder, folder_name)
                        folder_list[folder_name] = None
                    elif text == "Spam" and self.path != self.spam_folder and self.path != self.star_folder:
                        self.listbox.buttons[int(folder_name)].destroy()
                        self.listbox.update()
                        move_subfolder(self.path, self.spam_folder, folder_name)
                        folder_list[folder_name] = None
                    elif text == "Move" and self.path != self.move_to and self.path != self.star_folder:
                        self.listbox.buttons[int(folder_name)].destroy()
                        self.listbox.update()
                        print(self.path)
                        print(self.move_to)
                        move_subfolder(self.path, self.move_to, folder_name)
                        folder_list[folder_name] = None
                    else:
                        pass
            except Exception as e:
                print(e)

    def optionmenu_callback(self, choice):
    #   print("optionmenu dropdown clicked:", choice)
        self.move_to = os.path.join(self.user_folder, str(choice))
        self.clicked_handle("Move")
        self.combobox.destroy()
        self.combobox = None
        self.move_selected = False

    def create_combobox(self):
        self.combobox = CTkOptionMenu(
            master=self.tool_bar,
            values=["Inbox", "Trash", "Spam", "Work"],
            command=self.optionmenu_callback,
            variable=StringVar("")
        )
        self.combobox.grid(row=0, column=4, sticky="n")

    def update_content_frame(self, message, current_folder):
        self.tool_bar.back_button.grid()
        current_folder = os.path.dirname(current_folder)
        print(current_folder, "@@@")
    #    self.current_folder = os.path.join(self.path, str(message)) #check it
    #    print(self.current_folder)
        for widget in self.listbox.winfo_children():
            self.hide_widget(widget)
        self.show_email_content = ShowEmailContent(self.listbox, int(message), current_folder, Usermail)

    def hide_widget(self, widget):
        widget.pack_forget()

    def show_widget(self, widget):
        widget.pack()




