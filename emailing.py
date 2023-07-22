import smtplib # module to send mail
import imghdr # module to determine type of image
from email.message import EmailMessage

password = "ddafzhkebuwlhcws"
sender = "muditarora31@gmail.com"
receiver = "muditarora31@gmail.com"

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New Update of your room"
    email_message.set_content("Hey, looks like there has been movements in your room")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # sending mail
    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()

# checking
""" if __name__ == "__main__":
    send_email(image_path="images/image11.png")"""