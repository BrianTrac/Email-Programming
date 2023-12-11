# Import necessary modules
from tkinter import messagebox
from customtkinter import *
from PIL import Image


# Function to be executed when the search is processed
def process_search():
    messagebox.showinfo("Coming Soon", "This feature is coming soon!")


# Custom Tkinter frame for the search bar
class SearchBar(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        set_appearance_mode("dark")

        self.option_frame = None
        self.option_button = None
        self.create_widgets()

    def create_widgets(self):
        # Search bar
        search_bar = CTkFrame(self)
        search_bar.grid(row=0, column=0, sticky="nsew")

        # Create entry widget
        entry_widget = CTkLabel(search_bar, text_color="#FFCC70",
                                text="Search in mail box", font=("Helvetica", 16, "bold"),
                                width=640, height=40, corner_radius=32, fg_color="transparent",)
        entry_widget.pack(side="left", expand=True)

        # Create an option button with an icon
        option_image = Image.open("option_icon.png")
        self.option_button = CTkButton(search_bar, text="",
                                       image=CTkImage(dark_image=option_image, light_image=option_image),
                                       command=self.perform_option, width=50, height=30, fg_color="transparent")
        self.option_button.pack(side="right")

        # Adjust search_bar column weights to center entry_widget
        search_bar.columnconfigure(0, weight=1)
        search_bar.columnconfigure(1, weight=1)

    def perform_option(self):
        # Toggle the visibility of the option frame
        if self.option_frame is not None:
            # Destroy the search frame if it exists (to hide it)
            self.option_frame.destroy()
            self.option_frame = None
        else:
            # Create the search frame if it doesn't exist
            self.option_frame = CTkFrame(master=self.master)
            self.option_frame.grid(row=0, column=1)

            # Configure column and row weights for the search frame
            self.option_frame.columnconfigure(0, weight=2)
            self.option_frame.columnconfigure(1, weight=2)  # Adjust weight as needed
            self.option_frame.columnconfigure(2, weight=1)

            # List of information for widgets
            widget_info = [
                {"label_text": "To", "placeholder_text": "Enter sender email"},
                {"label_text": "Subject", "placeholder_text": "Enter subject"},
                {"label_text": "Content", "placeholder_text": "Enter content"}
            ]

            # Add widgets to the search frame using a for loop
            for row_index, info in enumerate(widget_info):
                # Add label
                CTkLabel(master=self.option_frame, text=info["label_text"], text_color="#5EE8FF",
                         font=("Helvetica", 12, "bold")).grid(row=row_index, column=0, pady=5, padx=25, sticky="ew")

                # Add entry widget
                CTkEntry(master=self.option_frame, placeholder_text=info["placeholder_text"],
                         text_color="#FFCC70", width=450).grid(row=row_index, column=1, pady=0, padx=25)

            # Add Search button in the bottom right corner
            search_button = CTkButton(master=self.option_frame, text="Search", command=self.on_search_button_click,
                                      width=50, height=20)
            search_button.grid(row=3, column=1, pady=0, padx=35, sticky="se")

    def on_search_button_click(self):
        # Handle the Search button click event
        # Perform search or any other actions if needed

        # Close the option_frame
        if self.option_frame is not None:
            self.option_frame.destroy()
            self.option_frame = None
        process_search()
