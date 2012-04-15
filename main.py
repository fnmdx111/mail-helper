# encoding: utf-8

import email
import imaplib
import config
from mail_utils import decode_from_address, decode_string, get_imap_server_from_address, get_mails_between, get_attachment_from_message


M = imaplib.IMAP4_SSL(get_imap_server_from_address(config.EMAIL_ADDRESS), 993)
M.login(config.EMAIL_ADDRESS, config.PASSWORD)
print('logging in')
M.select()
#type, data = M.search(None, 'UNSEEN')
#ids = data[0].split()
#for item in ids[::-1][:20]:
#    _, raw_data = M.fetch(item, '(RFC822)')
#
#    mail = email.message_from_string(raw_data[0][1])
#    subject = mail['subject']
#    print('subject:', decode_string(subject))
#    print('from:', decode_from_address(mail['from']))

for item in get_mails_between(M, unseen=True)[::-1][:10]:
    _, raw_data = M.fetch(item, '(RFC822)')

    mail = email.message_from_bytes(raw_data[0][1])
    subject = mail['subject']
    print('subject:', ''.join(decode_string(item) for item in subject.split()))
    print('from:', decode_from_address(mail['from']))
    print('id:', item)
    get_attachment_from_message(mail, 'as.gif')

M.close()
M.logout()




