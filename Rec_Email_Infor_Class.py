import json


class EmailInfo:
    def __init__(self, Date=None, To=None, Cc=None, From=None, Subject=None, Content_Transfer_Encoding=None):
        self.Date = Date
        self.To = To
        self.Cc = Cc
        self.From = From
        self.Subject = Subject
        self.Content_Transfer_Encoding = Content_Transfer_Encoding
        self.isRead = False

    def to_dict(self):
        return {
            'Date': self.Date,
            'To': self.To,
            'Cc': self.Cc,
            'From': self.From,
            'Subject': self.Subject,
            'Content_Transfer_Encoding': self.Content_Transfer_Encoding,
            'Read': self.isRead
        }

    def save_to_json(self, obj, filename):
        with open(filename, 'w') as file:
            json.dump(obj.to_dict(), file)

    def load_from_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return EmailInfo(data['Date'], data['To'], data['Cc'], data['From'], data['Subject'], data['Content_Transfer_Encoding'])

    def mark_as_read(self):
        self.isRead = True
