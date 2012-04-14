# encoding: utf-8

import email
import imaplib
import config
from mail_utils import decode_from_address, decode_string, guess_imap_server


M = imaplib.IMAP4_SSL(guess_imap_server(config.EMAIL_ADDRESS), 993)
M.login(config.EMAIL_ADDRESS, config.PASSWORD)
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




