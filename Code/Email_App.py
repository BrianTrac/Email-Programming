from customtkinter import *
from Logo import *
from Main import *
from Menu import *
from SearchBar import *


class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")

        # # Create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=5, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=5, uniform='a')

        # Create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=5, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')
        self.rowconfigure(1, weight=5, uniform='a')

        # Widgets
        self.logo = Logo(self)
        self.menu = Menu(self, callback = self.update_main_frame)
        self.main = Main(self)
        self.search_bar = SearchBar(self)
        
        self.logo.grid(row=0, column=0)
        self.menu.grid(row=1, column=0)
        self.main.grid(row=1, column=1, sticky="nsew")
        self.search_bar.grid(row=0, column=1)

        # run
        self.mainloop()

    def update_main_frame(self, message):
        self.main.update_main_frame(message)

App()
