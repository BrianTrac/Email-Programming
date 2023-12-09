from customtkinter import *
from Main import *

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self._set_appearance_mode("dark")

        # Create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=5, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=5, uniform='a')

        # Widgets
        self.menu = CTkFrame(self, fg_color="blue").grid(row=1, column=0, sticky="nsew")
        self.search_bar = CTkFrame(self, fg_color="green").grid(row=0, column=1, sticky="nsew")
        self.main = Main(self).grid(row=1, column=1, sticky="nsew")

        # run
        self.mainloop()


App()