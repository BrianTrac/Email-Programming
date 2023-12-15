from customtkinter import *
from PIL import Image
import json
import os
from move_folder import *

class ContentFrame(CTkFrame):
    def __init__(self, master, index, name, subject, time, cur_folder, callback):
        super().__init__(master)

        self.callback = callback
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.columnconfigure(3, weight=4, uniform='a')
        self.columnconfigure(4, weight=8, uniform='a')
        self.columnconfigure(5, weight=4, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        self.cur_folder = cur_folder
        self.index = index
        self.name = name
        self.subject = subject
        self.time = time
        self.json_path = os.path.join(self.cur_folder, "infor.json")
        with open(self.json_path) as json_file:
            data = json.load(json_file)

        self.mark_selected = False
        self.update_mark_status(self.mark_selected)
        self.in_yellow_star_folder = False
        try:
            self.star_selected = data["Star"]
            self.read_selected = data["Read"]
            # Used to check the previous folder which move the email to star folder
            self.prev_folder = data["Pre_Folder"]
        except Exception as e:
            print(e)

        self.folder_name = os.path.basename(self.cur_folder)
        self.source = os.path.dirname(self.cur_folder)
        self.star_folder = os.path.join(os.path.dirname(os.path.dirname(self.cur_folder)), "Star")

        self.bind('<Button-1>', self.command)
        self.create_widgets()

    def create_widgets(self):
        self.create_buttons()
        self.create_label()

    def create_buttons(self):
        # Create image
        mark_image = Image.open("assets\\mark_image.png").resize((20, 20))
        unmark_image = Image.open("assets\\unmark_image.png").resize((20, 20))
        white_star_image = Image.open("assets\\white_star_image.png").resize((20, 20))
        yellow_star_image = Image.open("assets\\yellow_star_image.png").resize((20, 20))
        read_image = Image.open("assets\\white_read_image.png").resize((20, 20))
        unread_image = Image.open("assets\\white_unread_image.png").resize((20, 20))

        # Create button
        self.unmark_button = CTkButton(self, text="", corner_radius=50, fg_color="transparent",
                                       hover_color="Gray31", command=lambda text="unmark": self.handle_command(text),
                                       image=CTkImage(dark_image=unmark_image, light_image=unmark_image, size=(20, 20)))
        self.mark_button = CTkButton(self, text="", corner_radius=50, fg_color="transparent",
                                     hover_color="Gray31", command=lambda text="mark": self.handle_command(text),
                                     image=CTkImage(dark_image=mark_image, light_image=mark_image, size=(20, 20)))
        self.white_star_button = CTkButton(self, text="", corner_radius=50, fg_color="transparent",
                                           hover_color="Gray31", command=lambda text="white_star": self.handle_command(text),
                                           image=CTkImage(dark_image=white_star_image, light_image=white_star_image, size=(20, 20)))
        self.yellow_star_button = CTkButton(self, text="", corner_radius=50, fg_color="transparent",
                                            hover_color="Gray31", command=lambda text="yellow_star": self.handle_command(text),
                                            image=CTkImage(dark_image=yellow_star_image, light_image=yellow_star_image, size=(20, 20)))
        self.read_button = CTkButton(self, text="", corner_radius=50, fg_color="transparent",
                                     hover_color="Gray31", command=lambda text="read": self.handle_command(text),
                                     image=CTkImage(dark_image=read_image, light_image=read_image, size=(20, 20)))
        self.unread_button = CTkButton(self, text="", corner_radius=50, fg_color="transparent",
                                       hover_color="Gray31", command=lambda text="unread": self.handle_command(text),
                                       image=CTkImage(dark_image=unread_image, light_image=unread_image, size=(20, 20)))

        # Check condition
        if self.mark_selected:
            self.mark_button.grid(row=0, column=0, sticky='nsw')
        else:
            self.unmark_button.grid(row=0, column=0, sticky='nsw')
        if self.star_selected == "True":
            self.yellow_star_button.grid(row=0, column=1, sticky='nsw')
        else:
            self.white_star_button.grid(row=0, column=1, sticky='nsw')
        if self.read_selected == "True":
            self.read_button.grid(row=0, column=2, sticky='nsw')
        else:
            self.unread_button.grid(row=0, column=2, sticky='nsw')

    def create_label(self):
        self.name_label = CTkLabel(self, text=self.name, font=("Helvetica", 12, "bold"))
        self.name_label.grid(row=0, column=3, sticky='nsew')
        self.name_label.bind('<Button-1>', command=self.command)
        self.name_label.bind('<Enter>', self.on_enter)
        self.name_label.bind('<Leave>', self.on_leave)

        self.subject_label = CTkLabel(self, text=self.subject, font=("Helvetica", 12, "bold"))
        self.subject_label.grid(row=0, column=4, sticky='nsew')
        self.subject_label.bind('<Button-1>', command=self.command)
        self.subject_label.bind('<Enter>', self.on_enter)
        self.subject_label.bind('<Leave>', self.on_leave)

        self.time_label = CTkLabel(self, text=self.time, font=("Helvetica", 12, "bold"))
        self.time_label.grid(row=0, column=5, sticky='nsew')
        self.time_label.bind('<Button-1>', command=self.command)
        self.time_label.bind('<Enter>', self.on_enter)
        self.time_label.bind('<Leave>', self.on_leave)

    def handle_command(self, text):
        if text == "mark":
            print("mark clicked")
            self.configure(fg_color="transparent")
            self.mark_button.grid_remove()
            self.unmark_button.grid(row=0, column=0, sticky='nsew')
            self.mark_selected = False
            self.update_mark_status(self.mark_selected)
        elif text == "unmark":
            print("unmark clicked")
            self.configure(fg_color="Mediumblue")
            self.unmark_button.grid_remove()
            self.mark_button.grid(row=0, column=0, sticky='nsew')
            self.mark_selected = True
            self.update_mark_status(self.mark_selected)
        elif text == "white_star":
            print("white_star clicked")
            self.white_star_button.grid_remove()
            self.yellow_star_button.grid(row=0, column=1, sticky='nsew')
            self.star_selected = True
            print(self.folder_name)
            if os.path.basename(self.source) == "Star":
                self.update_star_status(self.star_selected)
            else:
                self.prev_folder = self.source
                self.update_star_status(self.star_selected)
                delete_subfolder(self.star_folder, self.folder_name)
                copy_subfolder(self.source, self.star_folder, self.folder_name)
        elif text == "yellow_star":
            print("yellow_star clicked")
            self.yellow_star_button.grid_remove()
            self.white_star_button.grid(row=0, column=1, sticky='nsew')
            self.star_selected = False
            self.update_star_status(self.star_selected)
            print(self.source, self.folder_name)
            print(os.path.basename(self.source))
            if os.path.basename(self.source) == "Star":
                self.in_yellow_star_folder = True
                print(self.prev_folder)
                if os.path.basename(self.source) == "Star":
                    print("Star loop")
            else:
                delete_subfolder(self.star_folder, self.folder_name)
        elif text == "read":
            print("read clicked")
            self.read_button.grid_remove()
            self.unread_button.grid(row=0, column=2, sticky="nsew")
            self.read_selected = False
            self.update_read_status(self.read_selected)
        elif text == "unread":
            print("unread clicked")
            self.unread_button.grid_remove()
            self.read_button.grid(row=0, column=2, sticky="nsew")
            self.read_selected = True
            self.update_read_status(self.read_selected)
        else:
            pass

        # if self.in_yellow_star_folder:
        #     if not self.star_selected:
        #         self.in_yellow_star_folder = False
        #         delete_subfolder(self.prev_folder, self.folder_name)
        #         move_subfolder(self.source, self.prev_folder, self.folder_name)


    def update_read_status(self, is_read):
        # Open the file and load its contents into a dictionary
        with open(self.json_path, "r") as file:
            data = json.load(file)

        # Change the value in the dictionary
        data["Read"] = str(is_read)

        # Write the dictionary back to the file
        with open(self.json_path, "w") as file:
            json.dump(data, file)

    def update_star_status(self, is_star):
        # Open the file and load its contents into a dictionary
        with open(self.json_path, "r") as file:
            data = json.load(file)

        # Change the value in the dictionary
        data["Star"] = str(is_star)
        data["Pre_Folder"] = str(self.prev_folder)

        # Write the dictionary back to the file
        with open(self.json_path, "w") as file:
            json.dump(data, file)

    def update_mark_status(self, is_mark):
        # Open the file and load its contents into a dictionary
        with open(self.json_path, "r") as file:
            data = json.load(file)

        # Change the value in the dictionary
        data["Clicked"] = str(is_mark)

        # Write the dictionary back to the file
        with open(self.json_path, "w") as file:
            json.dump(data, file)

    def on_leave(self, event):
        if not self.mark_selected:
            self.configure(fg_color="transparent")

    def on_enter(self, event):
        if not self.mark_selected:
            self.configure(fg_color="DodgerBlue1")

    def command(self, event):
        self.handle_command("unread")
        print(self.cur_folder)
        print(f"Clicked {self.index} in {self.cur_folder}")
        self.callback(f"{self.index}", f"{self.cur_folder}")

