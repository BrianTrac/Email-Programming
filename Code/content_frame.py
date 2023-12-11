from customtkinter import * 
from PIL import Image

class ContentFrame(CTkFrame):
    def __init__(self, master, index=None, name=None, subject=None, time=None):
        super().__init__(master)
        
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.columnconfigure(3, weight=2, uniform='a')
        self.columnconfigure(4, weight=8, uniform='a')
        self.columnconfigure(5, weight=3, uniform='a')
        self.rowconfigure(0, weight=1, uniform='a')

        self.index = index
        self.name = name
        self.subject = subject
        self.time = time 
        self.unmark_selected = True
        self.white_star_selected = True
        self.unread_selected = True
        self.bind('<Button-1>', self.command)

        self.create_widgets()

    
    def create_widgets(self):
        self.create_buttons()
        self.create_label()
    
    def frame_command(self, event):
        print("Frame clicked!")
    
    def create_buttons(self):
        # Create image
        mark_image = Image.open("mark_image.png").resize((20,20))
        unmark_image = Image.open("unmark_image.png").resize((20,20))
        white_star_image = Image.open("white_star_image.png").resize((20,20))
        yellow_star_image = Image.open("yellow_star_image.png").resize((20,20))
        read_image = Image.open("white_read_image.png").resize((20,20))
        unread_image = Image.open("white_unread_image.png").resize((20,20))

        # Create button
        self.unmark_button = CTkButton(self, text = "", corner_radius=50, fg_color="transparent", 
                                hover_color="Gray31", command=lambda text="unmark": self.handle_command(text), 
                                image=CTkImage(dark_image=unmark_image, light_image=unmark_image, size=(20, 20)))
        self.mark_button = CTkButton(self, text = "", corner_radius=50, fg_color="transparent", 
                                hover_color="Gray31", command=lambda text="mark": self.handle_command(text), 
                                image=CTkImage(dark_image=mark_image, light_image=mark_image, size=(20, 20)))
        self.white_star_button = CTkButton(self, text = "", corner_radius=50, fg_color="transparent", 
                                hover_color="Gray31", command=lambda text="white_star": self.handle_command(text), 
                                image=CTkImage(dark_image=white_star_image, light_image=white_star_image, size=(20, 20)))
        self.yellow_star_button = CTkButton(self, text = "", corner_radius=50, fg_color="transparent", 
                                hover_color="Gray31", command=lambda text="yellow_star": self.handle_command(text), 
                                image=CTkImage(dark_image=yellow_star_image, light_image=yellow_star_image, size=(20, 20)))
        self.read_button = CTkButton(self, text = "", corner_radius=50, fg_color="transparent", 
                                hover_color="Gray31", command=lambda text="read": self.handle_command(text), 
                                image=CTkImage(dark_image=read_image, light_image=read_image, size=(20, 20)))
        self.unread_button = CTkButton(self, text = "", corner_radius=50, fg_color="transparent", 
                                hover_color="Gray31", command=lambda text="unread": self.handle_command(text), 
                                image=CTkImage(dark_image=unread_image, light_image=unread_image, size=(20, 20)))
       

        # Check condition
        if self.unmark_selected:
            self.unmark_button.grid(row=0, column=0, sticky='nsw')
        else:
            self.mark_button.grid(row=0, column=0, sticky='nsw')
        if self.white_star_selected:
            self.white_star_button.grid(row=0, column=1, sticky='nsw')
        else:
            self.yellow_star_button.grid(row=0, column=1, sticky='nsw')
        if self.unread_selected:
            self.unread_button.grid(row=0, column=2, sticky='nsw')
        else:
            self.read_button.grid(row=0, column=2, sticky='nsw')

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
            self.unmark_selected = True
        elif text == "unmark":
            print("unmark clicked")
            self.configure(fg_color="Mediumblue")
            self.unmark_button.grid_remove()
            self.mark_button.grid(row=0, column=0, sticky='nsew')
            self.unmark_selected = False
        elif text == "white_star":
            print("white_star clicked")
            self.white_star_button.grid_remove()
            self.yellow_star_button.grid(row=0, column=1, sticky='nsew')
            self.white_star_selected = False
        elif text == "yellow_star":
            print("yellow_star clicked")
            self.yellow_star_button.grid_remove()
            self.white_star_button.grid(row=0, column=1, sticky='nsew')
            self.white_star_selected = True
        elif text == "read":
            print("read clicked")
            self.read_button.grid_remove()
            self.unread_button.grid(row=0, column=2, sticky="nsew")
            self.unread_selected = True
        elif text == "unread":
            print("unread clicked")
            self.unread_button.grid_remove()
            self.read_button.grid(row=0, column=2, sticky="nsew")
            self.unread_selected=False
        else:
            pass

    def on_leave(self, event):
        if self.unmark_selected:
            self.configure(fg_color="transparent")

    def on_enter(self, event):
        if self.unmark_selected:
            self.configure(fg_color="DodgerBlue1")

    def command(self, event):
        print(f"Clicked {self.index}")

# if __name__ == "__main__":
#     root = CTk()
#     index = 0
#     name = "Brian Dang"
#     subject = "Hello World"
#     time = "19h30"
#     frame = ContentFrame(root, index, name, subject, time)
#     frame.configure(fg_color="DimGray")
#     frame.pack(expand=True, fill=BOTH)
#     root.mainloop()

    