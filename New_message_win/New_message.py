from customtkinter import *
from tkinter import messagebox
from PIL import Image
from Project.Send_main import send


class EmailApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1150x600+30+20")
        set_appearance_mode("dark")
        self.attachments = []
        self.create_widgets()

    def create_widgets(self):
        self.create_task_bar()
        self.create_tool_bar()
        self.create_infor_bar()
        self.create_text_box()
        self.fix()

    def create_task_bar(self):
        task_bar = CTkFrame(master=self.master)
        task_bar.grid(row=0, column=0, sticky="w")
        for i in range(8):
            task_bar.grid_columnconfigure(i, weight=1)

        task_buttons = [
            ("File", 0), ("Edit", 1), ("View", 2),
            ("Insert", 3), ("Format", 4), ("Options", 5),
            ("Tools", 6), ("Help", 7)
        ]

        for text, column in task_buttons:
            CTkButton(task_bar, text=text, font=("Helvetica", 12, "bold"),
                      fg_color="black").grid(row=0, column=column, pady=5, padx=0)

    def create_tool_bar(self):
        tool_bar = CTkFrame(master=self.master)
        tool_bar.grid(row=1, column=0, sticky="w")
        for i in range(2):
            tool_bar.grid_columnconfigure(i, weight=1)

        tool_buttons = [
            ("Send", "send_icon.png"), ("Save", "save_icon.png"),
            ("Attachment", "attachment_icon.png")
        ]

        for i, (text, image) in enumerate(tool_buttons):
            img = Image.open(f"New_message_win\\{image}")
            CTkButton(master=tool_bar, text=text, font=("Helvetica", 12, "bold"),
                      image=CTkImage(dark_image=img, light_image=img),
                      command=self.SendBtn if text == 'Send' else (self.choose_file if text == 'Attachment' else None)).grid(row=0, column=i, pady=5, padx=25)

    def create_infor_bar(self):
        infor_frame = CTkFrame(master=self.master)
        infor_frame.grid(row=2, column=0, sticky="w")
        infor_frame.grid_columnconfigure(1, weight=1)

        labels_entries = [
            ("From", "Enter sender email"),
            ("To", "Enter receive email"),
            ("Cc", "Enter Cc email"),
            ("Bcc", "Enter Bcc email"),
            ("Subject", "Enter subject")
        ]

        for i, (label_text, placeholder_text) in enumerate(labels_entries):
            CTkLabel(master=infor_frame, text=label_text, text_color="#5EE8FF", font=("Helvetica", 12, "bold")) \
                .grid(row=i, column=0, pady=5, padx=25, sticky="ew")
            CTkLabel(master=infor_frame, text="anhkhoa@gmail.com", fg_color='transparent',
                     text_color="#FFCC70", width=1400).grid(row=i, column=1, pady=5, padx=25)

        self.To = CTkEntry(
            master=infor_frame, placeholder_text="Enter receive email", text_color="#FFCC70", width=1400)
        self.To.grid(row=1, column=1, pady=5, padx=25)
        self.Cc = CTkEntry(
            master=infor_frame, placeholder_text="Enter Cc email", text_color="#FFCC70", width=1400)
        self.Cc.grid(row=2, column=1, pady=5, padx=25)
        self.BCc = CTkEntry(
            master=infor_frame, placeholder_text="Enter Bcc email", text_color="#FFCC70", width=1400)
        self.BCc.grid(row=3, column=1, pady=5, padx=25)
        self.Subject = CTkEntry(
            master=infor_frame, placeholder_text="Enter subject", text_color="#FFCC70", width=1400)
        self.Subject.grid(row=4, column=1, pady=5, padx=25)

    def create_text_box(self):
        # TextBox
        box_frame = CTkFrame(master=app)
        box_frame.grid(row=3, column=0, sticky="nsew")
        self.content = CTkTextbox(master=box_frame, scrollbar_button_color="#FFCC70", corner_radius=16, border_color="#FFCC70",
                                  border_width=2, text_color="#FFCC70")
        self.content.place(relx=0.5, rely=0.5, anchor="center",
                           relwidth=0.9, relheight=0.9)

    def fix(self):
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)
        self.master.grid_rowconfigure(3, weight=1)

    def choose_file(self):
        file_path = filedialog.askopenfilename(
            initialdir="/", title="Select a File", filetypes=(("All files", "*.*"), ("Text files", "*.txt*")))
        self.attachments.append(file_path)
        
    def SendBtn(self):
        to_email = self.To.get()
        cc_email = self.Cc.get()
        bcc_email = self.BCc.get()
        subject = self.Subject.get()
        content = self.content.get("1.0", "end-1c")
        recipient_email = ''
        # print(to_email, cc_email, bcc_email, subject, content)
        # print(self.attachments)
        send(
            "Anh Khoa",
            "anhkhoa@gmail.com",
            to_email,
            cc_email,
            bcc_email,
            subject,
            content,
            self.attachments)


if __name__ == "__main__":
    app = CTk()
    email_app = EmailApp(app)
    app.mainloop()
