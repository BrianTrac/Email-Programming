import os
import json
from customtkinter import *


class ShowEmailContent:
    def __init__(self, master, selected_email, path, user_email):
        self.master = master
        self.subject_frame_color = "#1A2F2B"
        self.infor_frame_color = "#2B2B2B"
        self.content_frame_color = "#2B2B2B"

        self.user_email = user_email
        self.selected_email = selected_email
        self.email_path = os.path.join(path, str(selected_email))
        self.json_path = os.path.join(
            self.email_path, 'infor.json')
        with open(self.json_path) as json_file:
            data = json.load(json_file)
            self.subject = data['Subject']
            self.sender = data['From']
            self.date = data['Date']

        self.create_frames()
        self.create_labels()
        self.create_textbox()
        self.update_attach_button()

    def create_frames(self):
        self.subject_frame = CTkFrame(
            master=self.master, fg_color=self.subject_frame_color)
        self.subject_frame.grid(row=0, column=0, sticky="nsew")

        self.infor_frame = CTkFrame(
            master=self.master, fg_color=self.infor_frame_color)
        self.infor_frame.grid(row=1, column=0, sticky="nsew")

        self.content_frame = CTkFrame(
            master=self.master, fg_color=self.content_frame_color)
        self.content_frame.grid(row=2, column=0, sticky="nsew")

        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def create_labels(self):
        SBJLabel = CTkLabel(master=self.subject_frame, text=self.subject, text_color="#FFFFFF",
                            font=("Helvetica", 12, "bold"))
        SBJLabel.pack(side="top", padx=10, pady=5)

        SenderLabel = CTkLabel(master=self.infor_frame, text="From :" + self.sender, text_color="#FFFFFF",
                               font=("Helvetica", 12, "bold"))
        SenderLabel.pack(side="left", padx=10, pady=5)

        with open(os.path.join(self.email_path, "infor.json"), "r") as file:
            data = json.load(file)
            if len(data['To']) != 0 or len(data['Cc']) != 0:
                if len(data['To']) != 0:
                    to = ""
                    for name in data["To"]:
                        to+=name+", "
                    to=to[:-2]
                    ToLabel = CTkLabel(master=self.infor_frame, text="To : "+to , text_color="#FFFFFF",
                                       font=("Helvetica", 12, "bold"))
                    ToLabel.pack(side="left", padx=10, pady=5)
                if len(data['Cc']) != 0:
                    cc = ""
                    for name in data["Cc"]:
                        cc += name+", "
                    cc = cc[:-2]
                    CcLabel = CTkLabel(master=self.infor_frame, text="Cc :"+ cc, text_color="#FFFFFF",
                                       font=("Helvetica", 12, "bold"))
                    CcLabel.pack(side="left", padx=10, pady=5)
            else:
                undisclosed_label = CTkLabel(master=self.infor_frame, text="To : undisclosed-recipients", text_color="#FFFFFF",
                                             font=("Helvetica", 12, "bold"))
                undisclosed_label.pack(side="left", padx=10, pady=5)

        DateLabel = CTkLabel(master=self.infor_frame, text=self.date, text_color="#FFFFFF",
                             font=("Helvetica", 12, "bold"))
        DateLabel.pack(side="right", padx=10, pady=5)

        self.AttachmentList = CTkButton(master=self.infor_frame, text="",
                                        text_color="#FFFFFF", fg_color="#2B2B2B",  state='disable', command=self.openFolder)
        self.AttachmentList.pack(side='right', padx=10, pady=10)

    def create_textbox(self):
        # Open the file and read its contents
        try:
            with open(os.path.join(self.email_path, 'content.txt'), "r") as file:
                file_contents = file.read()

        # Create a CTkTextbox and insert the file contents
            self.textbox = CTkTextbox(master=self.content_frame, scrollbar_button_color="#FFCC70",
                                      corner_radius=16, border_color="#FFCC70",
                                      border_width=2, text_color="#FFCC70", height=300)
            self.textbox.insert("1.0", file_contents)
            self.textbox.pack(side="top", fill="both",
                              expand=True, padx=10, pady=5)
        except Exception as e:
            print(e)

    def update_attach_button(self):
        items = os.listdir(self.email_path)
        if len(items) > 2:
            self.AttachmentList.configure(
                text=str(len(items) - 2) + " attachment(s)", state='normal', fg_color="#1A2F2B")
            for item in items:
                if item == "content.txt" or item == "infor.json":
                    continue
                else:
                    path = os.path.join(self.email_path, item)
                    CTkButton(master=self.content_frame, text=str(item), command=lambda event=path: self.open(
                        event), text_color="#FFFFFF", fg_color="#4158D0", hover_color="#C850C0", border_width=2).pack(side='left', padx=10, pady=10)

    def open(self, path):
        os.startfile(path)
    def openFolder(self):
        os.startfile(self.email_path)

    def open(self, path):
        os.startfile(path)

    def destroy_window(self):
        self.subject_frame.destroy()
        self.infor_frame.destroy()
        self.content_frame.destroy()



# if __name__ == "__main__":
#     root = CTk()
#     root.geometry("1150x600+30+20")
#     app = ShowEmailContent(root, 3, "D:/Python/Email App/Email-Programming-Brian/22120120@student.hcmus.edu.vn/Inbox", "22120120@student.hcmus.edu.vn")
#     root.mainloop()
