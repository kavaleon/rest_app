import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

message = MIMEMultipart('mixed')

message['Subject'] = 'text email'
message['From'] = 'gugushechk@gmail.com'
message['To'] = 'ulya-gonch15@yandex.ru'

text = 'Hello, how are u'
html = '''<html>
            <body style="background-image: url('https://i.pinimg.com/736x/1e/46/c2/1e46c2683f03cd969f6fb45e8a8083cf.jpg')">
                <h1>
                hhhh
                </h1>
                <p>test</p>
                <img src='cid:image1'>
            </body>
        </html>'''

message.attach(MIMEText(text, 'plain'))
message.attach(MIMEText(html, 'html'))

with open(r'D:\7eea9eb5eb0b4f7a084220b69ab7cdf4.png', 'rb') as img:
    image = MIMEImage(img.read())
    image.add_header('Content-ID', '<image1>')
    message.attach(image)

with open(r'D:\py_project\15102023\fgfg.txt', 'rb') as file:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename = "file.txt"')
    message.attach(part)

# with smtplib.SMTP_SSL('smtp.gmail.com', port=465) as server:
#     server.login('gugushechk@gmail.com', 'waqg bgbb dfnu zpbk')
#     server.sendmail(message["From"], message["To"], message.as_string())

with smtplib.SMTP('smtp.gmail.com', port=587) as server:
    server.starttls()
    server.login('gugushechk@gmail.com', 'waqg bgbb dfnu zpbk')
    server.sendmail(message["From"], message["To"], message.as_string())