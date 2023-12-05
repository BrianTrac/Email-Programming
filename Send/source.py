from functions import *


# Example usage
sender_name = 'Thinh'
sender_email = 'test@gmail.com'
subject = 'Test Subject'
message = 'Hello, this is TEST sending a message to Anh Khoa!'

to_email = 'anhkhoa@gmail.com'
# to_email
to_recipient_email = to_email.split(' ')
# Filter out empty strings
to_recipient_email = [email for email in to_recipient_email if email]
# cc_email
cc_email = "bcc@gmail.com"
cc_recipient_email = cc_email.split(' ')
# Filter out empty strings
cc_recipient_email = [email for email in cc_recipient_email if email]

# bcc_email
bcc_email = 'bcc@gmail.com'
bcc_recipient_email = bcc_email.split(' ')
# Filter out empty strings
bcc_recipient_email = [email for email in bcc_recipient_email if email]

recipient_email = set(to_recipient_email) | set(
    cc_recipient_email) | set(bcc_recipient_email)


attachment_path = []
MAX_SIZE = 20 * 1024 * 1024
cur_size = 0
while (True):
    path = input("Enter attachment path: ")
    if path == "":
        break
    elif not os.path.exists(path):
        print("File does not exist!\n")
    elif attachment_path.count(path) > 0:
        print("File is already exist!\n")
    elif cur_size + os.path.getsize(path) > MAX_SIZE:
        print("File is too large!\n")
    else:
        attachment_path.append(path)
        cur_size += os.path.getsize(path)


attachment_path = [os.path.normpath(raw_path) for raw_path in attachment_path]


send_email(
    sender_name,
    sender_email,
    recipient_email,
    to_recipient_email,
    cc_recipient_email,
    bcc_recipient_email,
    subject,
    message,
    attachment_path)
