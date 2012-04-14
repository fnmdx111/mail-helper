# encoding: utf-8

import base64
import datetime
import email
import re
import matcher


def get_server_from_address(type, address):
    return type + '.' + address.split('@')[1]


def get_smtp_server_from_address(address):
    return get_server_from_address('smtp', address)


def get_imap_server_from_address(address):
    return get_server_from_address('imap', address)


def decode_string(string):
    pattern = re.compile(r'=\?(.+?)\?B\?')
    match = pattern.search(string)
    if match:
        encoding = match.group(1)

        TRAIT = '?B?'

        return base64.b64decode(
                string[string.index(TRAIT) + len(TRAIT):].encode('ascii')
            ).decode(encoding)
    else:
        return string


def decode_from_address(from_address):
    if '"' in from_address:
        quote1 = from_address.index('"')
        quote2 = from_address.rindex('"')

        return '%s%s' % (decode_string(from_address[quote1:quote2 + 1]), from_address[quote2 + 1:])
    else:
        pattern = re.compile(r'(=\?.(.+?)\?B\?[^\s]+)')
        match = pattern.search(from_address)

        if match:
            encoded = match.group(1)
            raw = from_address[from_address.find(encoded) + len(encoded):]

            return '%s%s' % (decode_string(encoded), raw)
        else:
            return from_address


def transact_unseen_mails(mailbox, callback):
    _, data = mailbox.search(None, 'UNSEEN')

    for mail_id in data[0].split():
        _, raw_data = mailbox.fetch(mail_id, '(RFC822)')
        mail = email.message_from_string(raw_data[0][1])
        print('subject:', decode_string(mail['subject']))
        print('from:', decode_from_address(mail['from']))

        callback(mail)


def cb_mail(mail):
    pattern = re.compile(matcher.translate_pattern('世界英语概览 ({title: *}) {department: w} {name: w} {id: d}'), re.UNICODE)
    match = pattern.search(mail['from'])

    if not match:
        # send a match-fail email
        pass
    else:
        # send a match-succeed email
        pass


def get_mails_between(mail, before=None, since=None):
    """
        before and since should be 3-tuple as (year, month, day)
    """
    OK = 'OK'
    get_search_stmt = lambda obj, name: '%s %s' % (name, datetime.date(*obj).strftime(TIME_FORMAT)) if obj else ''
    TIME_FORMAT = '%d-%b-%Y'
    query = ('%s %s' % (
        get_search_stmt(before, 'BEFORE'),
        get_search_stmt(since, 'SINCE')
    )).strip() # 太恶心了，多了个空格，给的错误竟然还是cannot parse command，fuck
    if not before and not since:
        query = 'ALL'

    status, ids = mail.search(None, query)
    if status == OK:
        return ids[0].split()


