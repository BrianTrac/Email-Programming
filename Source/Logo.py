import customtkinter
from customtkinter import *
from tkinter import *
from PIL import Image
import os


class Logo(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        set_appearance_mode("dark")
        self.create_widgets()

    def create_widgets(self):
        image_path = os.path.join(os.path.dirname(__file__), 'assets\\logo.ico')
        image = customtkinter.CTkImage(light_image=Image.open(image_path), size=(100, 100))
        image_label = customtkinter.CTkLabel(self, image=image, text="")
        image_label.place(x=40, y=20)
