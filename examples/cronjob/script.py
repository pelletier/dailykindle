from datetime import timedelta
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import mimetypes
import dailykindle


f = open("sources.txt", "r")
feeds = f.readlines()
f.close()

dailykindle.build(feeds, '/tmp/', timedelta(1))
dailykindle.mobi('/tmp/daily.opf', 'bin/kindlegen')

msg = MIMEMultipart()
msg['From'] = 'me@myself.com'
msg['To'] = 'me@kindle.com'
msg['Subject'] = 'convert'

msg.attach(MIMEText(""))

ctype, encoding = mimetypes.guess_type('/tmp/daily.mobi')
if ctype is None or encoding is not None:
    ctype = 'application/octet-stream'
maintype, subtype = ctype.split('/', 1)


fp = open('/tmp/daily.mobi', 'rb')
part = MIMEBase(maintype, subtype)
part.set_payload(fp.read())
fp.close()
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename='daily.mobi')
msg.attach(part)

smtp = smtplib.SMTP('smtp.sendgrid.net', 587)
smtp.login('bar', 'foo')
smtp.sendmail('me@myself.com', ',e@kindle.com', msg.as_string())
smtp.close()
