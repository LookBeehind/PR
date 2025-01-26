import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import argparse

def send_email(from_email, to_email, subject, body, filename, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(from_email, password)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={filename}')
    msg.attach(part)

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    attachment.close()
    server.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send an email with an attachment')
    parser.add_argument('from_email', type=str, help='Sender email address')
    parser.add_argument('to_email', type=str, help='Receiver email address')
    parser.add_argument('subject', type=str, help='Subject of the email')
    parser.add_argument('body', type=str, help='Body of the email')
    parser.add_argument('filename', type=str, help='Path to the file to attach')
    parser.add_argument('password', type=str, help='Password for the sender email')

    args = parser.parse_args()
    send_email(args.from_email, args.to_email, args.subject, args.body, args.filename, args.password)
