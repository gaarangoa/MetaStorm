import smtplib, base64

#email.send_email('Gustavo Arango','cmetangen@gmail.com','RNATranscription2006.#','gaarangoa@gmail.com','testing','lets see if it works')

def send_email(uname, recipient, subject, body):
    import smtplib
    user='cmetangen@gmail.com';pwd='RNATranscription2006.#';gmail_user=user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body
# Prepare actual message
    message =  "\n".join(['From: MetaStorm <noreply@cmetann.com>','To: '+uname+' <'+recipient+'>','MIME-Version: 1.0','Content-type: text/html','Subject: '+subject,body])
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

