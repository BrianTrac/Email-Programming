from customtkinter import *

app = CTk()
app.geometry("1550x800-50")

set_appearance_mode("dark")

# Biến để theo dõi trạng thái của Label "CC"
cc_clicked = False

def toggle_cc(label):
    global cc_clicked
    cc_clicked = not cc_clicked

    # Thay đổi màu của Label "CC" khi được nhấp vào
    if cc_clicked:
        label.config(bg="green")
        insert_label = CTkLabel(master=tool_bar, text="New Label", font=("Helvetica", 12, "bold"), background=app.cget("background"))
        insert_label.grid(row=0, column=3, pady=5, padx=25)
        tool_bar.columnconfigure(3, weight=1)  # Cung cấp trọng số cột để chia sẻ không gian cột

    else:
        label.config(bg=app.cget("background"))
        # Xóa Label mới nếu đã được chèn
        for widget in tool_bar.grid_slaves():
            if int(widget.grid_info()["column"]) == 3:
                widget.destroy()


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
CTkLabel(master=tool_bar, text="", font=("Helvetica", 12, "bold")).grid(row=0, column=2, pady=5, padx=25)  # Empty column
CTkLabel(master=tool_bar, text="", font=("Helvetica", 12, "bold")).grid(row=0, column=3, pady=5, padx=25)  # Empty column
CTkLabel(master=tool_bar, text="", font=("Helvetica", 12, "bold")).grid(row=0, column=4, pady=5, padx=25)  # Empty column
cc_label = CTkLabel(master=tool_bar, text="CC", font=("Helvetica", 12, "bold"))
cc_label.grid(row=0, column=5, pady=5, padx=25)
cc_label.bind("<Button-1>", lambda event, label=cc_label: toggle_cc(label))
CTkLabel(master=tool_bar, text="BCC", font=("Helvetica", 12, "bold")).grid(row=0, column=6, pady=5, padx=25)  # Empty column
# Main Content Frame
frame_3 = CTkFrame(master=app)
frame_3.grid(row=2, column=1, sticky="w")  # Align left

CTkLabel(master=frame_3, text="From", text_color="#5EE8FF", font=("Helvetica", 12, "bold")).grid(row=0, column=0, pady=5, padx=25, sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter your username",text_color="#FFCC70", width=1400).grid(row=0, column=1, pady=5, padx=25)
CTkLabel(master=frame_3, text="To", text_color="#5EE8FF",font=("Helvetica", 12, "bold")).grid(row=1, column=0, pady=5, padx=25, sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter your password",text_color="#FFCC70", width=1400).grid(row=1, column=1, pady=5, padx=25)
CTkLabel(master=frame_3, text="Subject", text_color="#5EE8FF", font=("Helvetica", 12, "bold")).grid(row=2, column=0, pady=5, padx=25, sticky="e")
CTkEntry(master=frame_3, placeholder_text="Enter subject",text_color="#FFCC70", width=1400).grid(row=2, column=1, pady=5, padx=25)

# TextBox
textbox = CTkTextbox(master=app, scrollbar_button_color="#FFCC70", corner_radius=16, border_color="#FFCC70",
                     border_width=2, width=1300, height=475, text_color="#FFCC70")
textbox.place(relx=0.5, rely=0.6, anchor="center")

app.mainloop()
