from customtkinter import *
from tkinter import messagebox
from PIL import Image
from Send_main import send


class new_message_widget:
    def __init__(self, master,sender_name,sender_email):
        self.master = master
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.master.geometry("1200x800")
        set_appearance_mode("dark")
        self.attachments = []
        self.create_widgets()
        self.attachment_box = None

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
        self.tool_bar = CTkFrame(master=self.master)
        self.tool_bar.grid(row=1, column=0, sticky="w")
        for i in range(2):
            self.tool_bar.grid_columnconfigure(i, weight=1)

        tool_buttons = [
            ("Send", "send_icon.png"), ("Save", "save_icon.png"),
            ("Attachment", "attachment_icon.png")
        ]

        for i, (text, image) in enumerate(tool_buttons):
            img = Image.open(os.path.join(os.path.dirname(__file__), image))
            CTkButton(master=self.tool_bar, text=text, font=("Helvetica", 12, "bold"),
                      image=CTkImage(dark_image=img, light_image=img),
                      command=self.SendBtn if text == 'Send' else (self.choose_file if text == 'Attachment' else None)).grid(row=0, column=i, pady=5, padx=25)
        # Label to show number of attachments
        self.attachment_label = CTkLabel(
            master=self.tool_bar, text="", fg_color='transparent')
        # adjust the position as needed
        self.attachment_label.grid(row=0, column=3, pady=5, padx=25)

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
            CTkLabel(master=infor_frame, text=self.sender_email, fg_color='transparent',
                     text_color="#FFCC70", width=1400).grid(row=i, column=1, pady=5, padx=25)

        self.To = CTkEntry(
            master=infor_frame, placeholder_text="Enter receive email", text_color="#FFCC70", width=1400)
        self.To.grid(row=1, column=1, pady=5, padx=25)
        self.Cc = CTkEntry(
            master=infor_frame, placeholder_text="Enter Cc email", text_color="#FFCC70", width=1400)
        self.Cc.grid(row=2, column=1, pady=5, padx=25)
        self.Bcc = CTkEntry(
            master=infor_frame, placeholder_text="Enter Bcc email", text_color="#FFCC70", width=1400)
        self.Bcc.grid(row=3, column=1, pady=5, padx=25)
        self.Subject = CTkEntry(
            master=infor_frame, placeholder_text="Enter subject", text_color="#FFCC70", width=1400)
        self.Subject.grid(row=4, column=1, pady=5, padx=25)

    def create_text_box(self):
        # TextBox
        box_frame = CTkFrame(master=self.master)
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
        if file_path not in self.attachments:
            self.attachments.append(file_path)
            self.attachment_label.configure(
                # update the label
                text=str(len(self.attachments))+' attachment(s)')

            self.attachment_box = CTkComboBox(
                master=self.tool_bar, fg_color="#B816B4", border_color="#FFCC70", border_width=2,
                values=self.attachments, state='readonly')
            self.attachment_box.grid(row=0, column=4, pady=5, padx=25)

    def SendBtn(self):
        to_email = self.To.get()
        cc_email = self.Cc.get()
        bcc_email = self.Bcc.get()
        subject = self.Subject.get()
        content = self.content.get("1.0", "end-1c")
        recipient_email = ''
        # print(to_email, cc_email, bcc_email, subject, content)
        # print(self.attachments)
        if to_email == '':
            messagebox.showerror("Error", "Please enter the recipient's email")
        else:
            send(self.sender_name, self.sender_email, to_email, cc_email,
                 bcc_email, subject, content, self.attachments)

            # Clear input after send
            self.To.delete(0, END)
            self.Cc.delete(0, END)
            self.Bcc.delete(0, END)
            self.Subject.delete(0, END)
            self.content.delete("1.0", END)
            messagebox.showinfo(
                "Success", "Your email has been sent successfully")
            self.attachment_label.configure(text="")
            self.attachment_box.destroy()
            self.attachments = []
            
# if __name__ == "__main__":
#     root = CTk()
#     new_message_widget(root,"Anh Khoa","anhkhoa@gmail.com")
#     root.mainloop()