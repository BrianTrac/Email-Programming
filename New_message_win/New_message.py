from customtkinter import *
from tkinter import messagebox
from PIL import Image


def comming_soon():
    messagebox.showinfo("Coming Soon", "This feature is coming soon!")


app = CTk()
app.geometry("1150x600+30+20")

set_appearance_mode("dark")

# Task Bar
task_bar = CTkFrame(master=app)
task_bar.grid(row=0, column=0, sticky="w")
for i in range(8):
    task_bar.grid_columnconfigure(i, weight=1)
# Tool Bar (Below Task Bar)
tool_bar = CTkFrame(master=app)
tool_bar.grid(row=1, column=0, sticky="w")
for i in range(2):
    tool_bar.grid_columnconfigure(i, weight=1)
# Main Content
frame_3 = CTkFrame(master=app)
frame_3.grid(row=2, column=0, sticky="w")

# TextBox
box_frame = CTkFrame(master=app)
box_frame.grid(row=3, column=0, sticky="nsew")
for i in range(5):
    app.grid_columnconfigure(i, weight=1 if i ==0 else 0)
app.grid_rowconfigure(3, weight=1)


CTkButton(task_bar, text="File", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=0, pady=5, padx=0)
CTkButton(task_bar, text="Edit", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=1, pady=5, padx=0)
CTkButton(task_bar, text="View", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=2, pady=5, padx=0)
CTkButton(task_bar, text="Insert", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=3, pady=5, padx=0)
CTkButton(task_bar, text="Format", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=4, pady=5, padx=0)
CTkButton(task_bar, text="Options", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=5, pady=5, padx=0)
CTkButton(task_bar, text="Tools", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=6, pady=5, padx=0)
CTkButton(task_bar, text="Help", font=("Helvetica", 12, "bold"),
          fg_color="black", command=comming_soon).grid(row=0, column=7, pady=5, padx=0)


send_img = Image.open("New_message_win\\send_icon.png")
CTkButton(master=tool_bar, text="Send", font=("Helvetica", 12, "bold"),
          image=CTkImage(dark_image=send_img, light_image=send_img),
          command=comming_soon).grid(row=0, column=0, pady=5, padx=25)
save_img = Image.open("New_message_win\\save_icon.png")
CTkButton(master=tool_bar, text="Save", font=("Helvetica", 12, "bold"),
          image=CTkImage(dark_image=save_img, light_image=save_img),
          command=comming_soon).grid(row=0, column=1, pady=5, padx=25)

frame_3.grid_columnconfigure(1, weight=1)
CTkLabel(master=frame_3, text="From", text_color="#5EE8FF", font=(
    "Helvetica", 12, "bold")).grid(row=0, column=0, pady=5, padx=25, sticky="ew")
CTkEntry(master=frame_3, placeholder_text="Enter sender email",
         text_color="#FFCC70", width=1400).grid(row=0, column=1, pady=5, padx=25)
CTkLabel(master=frame_3, text="To", text_color="#5EE8FF", font=(
    "Helvetica", 12, "bold")).grid(row=1, column=0, pady=5, padx=25, sticky="ew")
CTkEntry(master=frame_3, placeholder_text="Enter receive email",
         text_color="#FFCC70", width=1400).grid(row=1, column=1, pady=5, padx=25)
CTkLabel(master=frame_3, text="CC", text_color="#5EE8FF", font=(
    "Helvetica", 12, "bold")).grid(row=2, column=0, pady=5, padx=25, sticky="ew")
CTkEntry(master=frame_3, placeholder_text="Enter receive email",
         text_color="#FFCC70", width=1400).grid(row=2, column=1, pady=5, padx=25)
CTkLabel(master=frame_3, text="BCC", text_color="#5EE8FF", font=(
    "Helvetica", 12, "bold")).grid(row=3, column=0, pady=5, padx=25, sticky="ew")
CTkEntry(master=frame_3, placeholder_text="Enter receive email",
         text_color="#FFCC70", width=1400).grid(row=3, column=1, pady=5, padx=25)
CTkLabel(master=frame_3, text="Subject", text_color="#5EE8FF", font=(
    "Helvetica", 12, "bold")).grid(row=4, column=0, pady=5, padx=25, sticky="ew")
CTkEntry(master=frame_3, placeholder_text="Enter subject",
         text_color="#FFCC70", width=1400).grid(row=4, column=1, pady=5, padx=25)


CTkTextbox(master=box_frame, scrollbar_button_color="#FFCC70", corner_radius=16, border_color="#FFCC70",
           border_width=2, text_color="#FFCC70").place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)


attachment_img = Image.open("New_message_win\\attachment_icon.png")
btn = CTkButton(master=tool_bar, text="Attachment", corner_radius=32, fg_color="#4158D0", hover_color="#C850C0",
                border_color="#FFCC70", border_width=2, image=CTkImage(dark_image=attachment_img, light_image=attachment_img),
                command=comming_soon)
btn.grid(row=0, column=2, pady=5, padx=25)

app.mainloop()
