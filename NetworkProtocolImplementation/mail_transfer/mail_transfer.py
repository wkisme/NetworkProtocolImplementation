# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage
textfile = '/home/wangkuo/PycharmProjects/NetworkProtocolImplementation/gui/README'


def mail_transfer():
    # Open the plain text file whose name is in textfile for reading.
    with open(textfile) as fp:
        # Create a text/plain message
        msg = EmailMessage()
        msg.set_content(fp.read())

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = 'The contents of %s' % textfile
    msg['From'] = '1476377353@qq.com'
    msg['To'] = '1476377353@qq.com'

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('smtp.qq.com')

    s.login('1476377353@qq.com', 'tbqokxospxetbagf')
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':

    mail_transfer()
