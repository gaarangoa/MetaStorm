import smtplib
import base64
import os


def send_email(uname, recipient, subject, body):
    import smtplib
    user = os.environ['email']
    pwd = os.environ['epass']
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]

    message = "\n".join(['From: MetaStorm <noreply@cmetann.com>', 'To: '+uname+' <'+recipient +
                         '>', 'MIME-Version: 1.0', 'Content-type: text/html', 'Subject: '+subject, body])
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        return True
    except:
        return False
