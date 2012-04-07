# encoding: utf-8

import email
import imaplib
from mail_utils import decode_from_address, decode_string


M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
M.login('chsc4698@gmail.com', '')
print 'logging in'
M.select()
type, data = M.search(None, 'UNSEEN')
ids = data[0].split()
for item in ids[::-1][:20]:
    _, raw_data = M.fetch(item, '(RFC822)')

    mail = email.message_from_string(raw_data[0][1])
    subject = mail['subject']
    print 'subject:', decode_string(subject)
    print 'from:', decode_from_address(mail['from'])


M.close()
M.logout()




