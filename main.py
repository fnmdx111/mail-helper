# encoding: utf-8
import base64
import email
import imaplib
import re
import matcher


M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
M.login('chsc4698@gmail.com', 'staCraft1**')
print 'logging in'
M.select()
type, data = M.search(None, 'ALL')
ids = data[0].split()
for item in ids[::-1][:20]:
    _, raw_data = M.fetch(item, '(RFC822)')

    mail = email.message_from_string(raw_data[0][1])
    subject = mail['subject']
    print 'subject:', decode_string(subject)
    print 'from:', decode_from_address(mail['from'])


M.close()
M.logout()




