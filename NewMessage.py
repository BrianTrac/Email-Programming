from customtkinter import *
from PIL import Image

app = CTk()
app.geometry("1550x800-50")

set_appearance_mode("dark")

# Task Bar
task_bar = CTkFrame(master=app)
task_bar.grid(row=0, column=1, sticky="w")  # Align left

CTkLabel(master=task_bar, text="File", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=5, padx=25)
CTkLabel(master=task_bar, text="Edit", font=("Helvetica", 12, "bold")).grid(row=0, column=1, pady=5, padx=25)
CTkLabel(master=task_bar, text="View", font=("Helvetica", 12, "bold")).grid(row=0, column=2, pady=5, padx=25)
CTkLabel(master=task_bar, text="Insert", font=("Helvetica", 12, "bold")).grid(row=0, column=3, pady=5, padx=25)
CTkLabel(master=task_bar, text="Format", font=("Helvetica", 12, "bold")).grid(row=0, column=4, pady=5, padx=25)
CTkLabel(master=task_bar, text="Options", font=("Helvetica", 12, "bold")).grid(row=0, column=5, pady=5, padx=25)
CTkLabel(master=task_bar, text="Tools", font=("Helvetica", 12, "bold")).grid(row=0, column=6, pady=5, padx=25)
CTkLabel(master=task_bar, text="Help", font=("Helvetica", 12, "bold")).grid(row=0, column=7, pady=5, padx=25)

# Tool Bar (Below Task Bar)
tool_bar = CTkFrame(master=app)
tool_bar.grid(row=1, column=1, sticky="w")  # Align left

CTkLabel(master=tool_bar, text="Send", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=5, padx=25)
CTkLabel(master=tool_bar, text="Save", font=("Helvetica", 12, "bold")).grid(row=0, column=1, pady=5, padx=25)
# CTkLabel(master=tool_bar, text="", font=("Helvetica", 12, "bold")).grid(row=0, column=2, pady=5,
#                                                                         padx=25)  # Empty column
# CTkLabel(master=tool_bar, text="", font=("Helvetica", 12, "bold")).grid(row=0, column=3, pady=5,
#                                                                         padx=25)  # Empty column
# CTkLabel(master=tool_bar, text="", font=("Helvetica", 12, "bold")).grid(row=0, column=4, pady=5,
#                                                                         padx=25)  # Empty column
# Main Content Frame
frame_3 = CTkFrame(master=app)
frame_3.grid(row=4, column=1, sticky="w")  # Align left

CTkLabel(master=frame_3, text="From", text_color="#5EE8FF", font=("Helvetica", 12, "bold")).grid(row=0, column=0,
                                                                                                 pady=5, padx=25,
                                                                                                 sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter sender email", text_color="#FFCC70", width=1400).grid(row=0, column=1,
                                                                                                        pady=5, padx=25)
CTkLabel(master=frame_3, text="To", text_color="#5EE8FF", font=("Helvetica", 12, "bold")).grid(row=1, column=0, pady=5,
                                                                                               padx=25, sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter receive email", text_color="#FFCC70", width=1400).grid(row=1, column=1,
                                                                                                        pady=5, padx=25)
CTkLabel(master=frame_3, text="CC", text_color="#5EE8FF", font=("Helvetica", 12, "bold")).grid(row=2, column=0,
                                                                                                    pady=5, padx=25,
                                                                                                    sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter receive email", text_color="#FFCC70", width=1400).grid(row=2, column=1,
                                                                                                  pady=5, padx=25)
CTkLabel(master=frame_3, text="BCC", text_color="#5EE8FF", font=("Helvetica", 12, "bold")).grid(row=3, column=0,
                                                                                                    pady=5, padx=25,
                                                                                                    sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter receive email", text_color="#FFCC70", width=1400).grid(row=3, column=1,
                                                                                                  pady=5, padx=25)
CTkLabel(master=frame_3, text="Subject", text_color="#5EE8FF", font=("Helvetica", 12, "bold")).grid(row=4, column=0,
                                                                                                    pady=5, padx=25,
                                                                                                    sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter subject", text_color="#FFCC70", width=1400).grid(row=4, column=1,
                                                                                                  pady=5, padx=25)

img = Image.open("attachment_icon.png")
btn = CTkButton(master=app, text="Attachment", corner_radius=32, fg_color="#4158D0",
                hover_color="#C850C0", border_color="#FFCC70",
                border_width=2, image=CTkImage(dark_image=img, light_image=img))
btn.place(relx=0.875, rely=0.07, anchor="center")

# TextBox
textbox = CTkTextbox(master=app, scrollbar_button_color="#FFCC70", corner_radius=16, border_color="#FFCC70",
                     border_width=2, width=1300, height=475, text_color="#FFCC70")
textbox.place(relx=0.5, rely=0.65, anchor="center")

app.mainloop()
