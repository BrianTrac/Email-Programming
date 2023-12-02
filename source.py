from functions import *


# Example usage
sender_name = 'Thinh'
sender_email = 'anhkhoa@gmail.com'
subject = 'Test Subject'
message = 'Hello, this is a Python agent sending a message!'

to_email ='test@gmail.com'
# to_email
to_recipient_email = to_email.split(' ')
# Filter out empty strings
to_recipient_email = [email for email in to_recipient_email if email]

#cc_email
cc_email = "test@gmail.com"
cc_recipient_email = cc_email.split(' ')
# Filter out empty strings
cc_recipient_email = [email for email in cc_recipient_email if email]

#bcc_email
bcc_email = 'test@gmail.com'
bcc_recipient_email = bcc_email.split(' ')
# Filter out empty strings
bcc_recipient_email = [email for email in bcc_recipient_email if email]

recipient_email = set(to_recipient_email) | set(cc_recipient_email) | set(bcc_recipient_email)

attachment_path = ["E:\Data_Structures_And_Algorithms\Challenge1\input.txt",
                   "E:\pixel.pdf",
                   "E:\pixel.png"]


send_email(sender_name, sender_email, recipient_email, to_recipient_email,
           cc_recipient_email, bcc_recipient_email, subject, message,attachment_path)
