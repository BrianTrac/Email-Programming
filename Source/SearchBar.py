# Import necessary modules
from tkinter import messagebox
from customtkinter import *
from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkImage
from PIL import Image
import json

# Custom Tkinter frame for the search bar
class SearchBar(CTkFrame):
    def __init__(self, master, callback):
        super().__init__(master)
        set_appearance_mode("dark")

        self.callback = callback
        self.option_frame = None
        self.option_button = None
        self.create_widgets()

    def create_widgets(self):
        # Search bar
        self.search_bar = CTkFrame(self)
        self.search_bar.grid(row=0, column=0, sticky="nsew")
        # Adjust search_bar column weights to center entry_widget
        self.search_bar.columnconfigure(0, weight=1)
        self.search_bar.columnconfigure(1, weight=1)

##############################################################################################
        self.setting_frame = CTkFrame(self)
        self.setting_frame.grid(row=0, column=1, sticky="nsew")

        self.settingBtn=CTkButton(self.setting_frame, text="Setting", command=self.setting_func)
        self.settingBtn.pack(side="right", padx=10)
        # Create entry widget
        self.entry_widget = CTkLabel(self.search_bar, text_color="#FFCC70",
                                text="Search in mail box", font=("Helvetica", 16, "bold"),
                                width=640, height=40, corner_radius=32, fg_color="transparent",)
        self.entry_widget.pack(side="left", expand=True)

        # Create an option button with an icon
        option_image = Image.open("assets\\option_icon.png")
        self.option_button = CTkButton(self.search_bar, text="",
                                       image=CTkImage(
                                           dark_image=option_image, light_image=option_image),
                                       command=self.perform_option, width=50, height=30, fg_color="transparent")
        self.option_button.pack(side="right", padx=10)


    def perform_option(self):
        # Toggle the visibility of the option frame
        # print("Perform option")
        if self.option_frame is not None:
            # Destroy the search frame if it exists (to hide it)
            self.option_frame.destroy()
            self.option_frame = None
        else:
            # Create the search frame if it doesn't exist
            self.option_frame = CTkFrame(master=self.master)
            self.option_frame.grid(row=0, column=1, sticky="w")

            # Configure column and row weights for the search frame
            self.option_frame.columnconfigure(0, weight=2)
            self.option_frame.columnconfigure(1, weight=2)
            self.option_frame.columnconfigure(2, weight=1)
            self.option_frame.columnconfigure(3, weight=1)

            # List of information for widgets
            widget_info = [
                {"label_text": "To", "placeholder_text": "Enter sender email"},
                {"label_text": "From", "placeholder_text": "Enter from"},
                {"label_text": "Subject", "placeholder_text": "Enter subject"},
                {"label_text": "Content", "placeholder_text": "Enter content"},
            ]

            # Add widgets to the search frame using a for loop
            for row_index, info in enumerate(widget_info):
                # Add label
                CTkLabel(master=self.option_frame, text=info["label_text"], text_color="#5EE8FF",
                         font=("Helvetica", 12, "bold")).grid(row=row_index, column=0, pady=5, padx=25, sticky="ew")

            # Add entry widget
            self.To = CTkEntry(master=self.option_frame, placeholder_text="Enter sender email",
                               text_color="#FFCC70", width=450)
            self.To.grid(row=0, column=1, pady=0, padx=25)

            self.From = CTkEntry(master=self.option_frame, placeholder_text="Enter from",
                                 text_color="#FFCC70", width=450)
            self.From.grid(row=1, column=1, pady=0, padx=25)

            self.Subject = CTkEntry(master=self.option_frame, placeholder_text="Enter subject",
                                    text_color="#FFCC70", width=450)
            self.Subject.grid(row=2, column=1, pady=0, padx=25)

            self.Content = CTkEntry(master=self.option_frame, placeholder_text="Enter content",
                                    text_color="#FFCC70", width=450)
            self.Content.grid(row=3, column=1, pady=0, padx=25)

            # Add Search button in the bottom right corner
            search_button = CTkButton(master=self.option_frame, text="Search", command=self.on_search_button_click,
                                      width=50, height=20)
            search_button.grid(row=4, column=1, pady=0, padx=35, sticky="se")

    def on_search_button_click(self):
        # Handle the Search button click event
        # Perform search or any other actions if needed
        self.process_search()

        # Close the option_frame
        if self.option_frame is not None:
            self.option_frame.destroy()
            self.option_frame = None

    def process_search(self):
        To = self.To.get()
        From = self.From.get()
        Subject = self.Subject.get()
        Content = self.Content.get()
        # print(To, From, Subject, Content)
        self.callback(To, From, Subject, Content)

    def setting_func(self):
        self.settingBtn.pack_forget()
        self.search_bar.grid_forget()
        
        try:
            with open('config.json', 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(e)
        
        self.POP3_PORT = CTkEntry(self.setting_frame)
        self.POP3_PORT.insert(0, data["POP3"])
        self.POP3_PORT.grid(row=0, column=1, sticky="nsew")
        self.POP3_PORT_text = CTkLabel(self.setting_frame, text="POP3 PORT", text_color="#5EE8FF")
        self.POP3_PORT_text.grid(row=0, column=0, sticky="nsew")

        self.SMTP_PORT = CTkEntry(self.setting_frame)
        self.SMTP_PORT.insert(0, data["SMTP"])
        self.SMTP_PORT.grid(row=1, column=1, sticky="nsew")
        self.SMTP_PORT_text = CTkLabel(self.setting_frame, text="SMTP PORT", text_color="#5EE8FF")
        self.SMTP_PORT_text.grid(row=1, column=0, sticky="nsew")

        self.Autoload = CTkEntry(self.setting_frame)
        self.Autoload.insert(0, data["Autoload"])
        self.Autoload.grid(row=2, column=1, sticky="nsew")
        self.Autoload_text = CTkLabel(self.setting_frame, text="Autoload (s)", text_color="#5EE8FF")
        self.Autoload_text.grid(row=2, column=0, sticky="nsew")

        self.max_size = CTkEntry(self.setting_frame)
        self.max_size.insert(0, data["MAX"])
        self.max_size.grid(row=3, column=1, sticky="nsew")
        self.max_size_text = CTkLabel(self.setting_frame, text="Max size (MB)", text_color="#5EE8FF")
        self.max_size_text.grid(row=3, column=0, sticky="nsew")

        # save and quit button
        self.SAQFrame=CTkFrame(self.setting_frame)
        self.SAQFrame.grid(row=4, column=1, sticky="nsew")
        
        self.saveBtn=CTkButton(self.SAQFrame,command=self.save_func, text="Save")
        self.saveBtn.grid(row=0, column=0, sticky="nsew")
        
        self.quitBtn=CTkButton(self.SAQFrame,command=self.close, text="Quit")
        self.quitBtn.grid(row=0, column=1, sticky="nsew")
        
    def save_func(self):
        
        POP3_PORT = self.POP3_PORT.get()
        SMTP_PORT = self.SMTP_PORT.get()
        Autoload = self.Autoload.get()
        max_size = self.max_size.get()
        
        if POP3_PORT == "" or SMTP_PORT == "" or Autoload == "" or max_size == "":
            messagebox.showerror("Error", "Please fill all the fields")
            return
        
        try :
            with open('config.json', 'r') as f:
                data = json.load(f)
            data["SMTP"] = SMTP_PORT
            data["POP3"] = POP3_PORT
            data["Autoload"] = Autoload
            data["MAX"] = max_size

            # Write the data back to the file
            with open('config.json', 'w') as f:
                json.dump(data, f)    
            messagebox.showinfo("Success", "Save successfully")

            self.close()
                 
                           
        except Exception as e:
            messagebox.showerror("Error", "Can't open config.json")
            return

    def close(self):
        self.POP3_PORT.grid_forget()
        self.SMTP_PORT.grid_forget()
        self.Autoload.grid_forget()
        self.max_size.grid_forget()
        self.saveBtn.grid_forget()
        self.quitBtn.grid_forget()
        self.SAQFrame.grid_forget()
        self.POP3_PORT_text.grid_forget()
        self.SMTP_PORT_text.grid_forget()
        self.Autoload_text.grid_forget()
        self.max_size_text.grid_forget()
        
        self.search_bar.grid(row=0, column=0, sticky="nsew")
        self.search_bar.columnconfigure(0, weight=1)
        self.search_bar.columnconfigure(1, weight=1)  
        
        self.settingBtn.pack(side="right", padx=10)