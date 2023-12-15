from customtkinter import *
from Logo import *
from Main import *
from Menu import *
from SearchBar import *
from Receive_email import get_email
from threading import Thread

class App(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700+300+50")

        # # Create the grid
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=5, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=6, uniform='a')

        # Widgets
        self.logo = Logo(self)
        self.menu = Menu(self, callback=self.update_main_frame)
        self.main = Main(self)
        self.search_bar = SearchBar(self, callback=self.update_main_search_frame)
        
        self.logo.grid(row=0, column=0)
        self.menu.grid(row=1, column=0)
        self.main.grid(row=1, column=1, sticky="nsew")
        self.search_bar.grid(row=0, column=1)

        try:
            with open('config.json', 'r') as f:
                self.data = json.load(f)
        except Exception as e:
            print(e)

        print("START PRINT THREAD")
        try:
            self.start_print_thread()

        except Exception as e:
            print(e)
        # run
        self.mainloop()

    # Autoload
    def start_print_thread(self):
        def print_time_sleep():
            while True:
                print("TIME SLEEP")
                time.sleep(int(self.data["Autoload"]))
                get_email(self.data["Usermail"], self.data["PASS"], self.data["MailServer"], int(self.data["POP3"]))

        thread = Thread(target=print_time_sleep, daemon=True)
        thread.start()

    def update_main_frame(self, message):
        self.main.update_main_frame(message)

    def update_main_search_frame(self, To, From, Subject, Message):
        self.main.update_main_search_frame(To, From, Subject, Message)

App()
