# encoding: utf-8

import re


SPACE_AWARE = False
def translate_pattern(raw_pattern):
    META_CHARACTERS = [u'.', u'^', u'$', u'*', u'+', u'?', u'\\', u'{', u'}', u'[', u']', u'(', u')', u'|']

    raw_chunks = raw_pattern.replace(u'{', u'%').replace(u'}', u'$%').split(u'%')

    def _translate_sub_pattern(sub_raw_pattern):
        substitution = {
            'w': '\\w',
            'd': '\\d',
            '*': '.'
        }

        pattern = re.compile(r'(?P<param>[^:]+):\s*(?P<type>[*wd]\d*)')
        match = pattern.search(sub_raw_pattern)

        if match:
            match_dict = match.groupdict()
            type_suffix = '+' if len(match_dict['type']) < 2 else '{%s}' % match_dict['type'][1:]
            return r'(?P<%s>%s)' % (match_dict['param'], substitution[match_dict['type'][0]] + type_suffix)

        return None


    def escape_re(string):
        result = [u'\\' + i if i in META_CHARACTERS else i for i in string]

        return u''.join(result)


    chunks = []
    for item in raw_chunks:
        if len(item) > 0 and item[-1] == '$':
            # it's a sub_pattern
            chunks.append(_translate_sub_pattern(item))
        else:
            if not SPACE_AWARE:
                s = escape_re(item)
                s = re.compile(r'\s+').sub(r'\s*', s)
                chunks.append(s)
            else:
                chunks.append(escape_re(item))

    return ''.join(chunks) + '$'


# notes on how to write a pattern
# substitute the variables with {variable_name: criteria}
# where criteria := type[count]
# supported types are w: word, d: digit, *: wildcard
# if you want to match the type `count` times, e.g. match w 4 times => w4
# e.g. 第几次课 - 姓名 - 某专业几班 - 学号 =>
# '第{course: d}次课 - {name: w} - {major: w}{class_number: d}班 - {id: d13}'
# some tips:
# do not have adjacent criteria of the same type, or it may still match subjects, but the outcomes may be wrong
# if a variable may contain space, you may want to enclose the variable with parentheses, or it may still match subjects, but the outcomes may be wrong
# e.g. 世界英语概览 标题 学院 姓名 学号：xxx
# 世界英语概览 ({title: *}) {department: w} {name: w} 学号: {id: d}

if __name__ == '__main__':
    test = translate_pattern(u'第{course: d}次课 - {name: w} - {major: w}{class_number: d}班 - {id: d13}')
    #test = translate_pattern(u'世界英语概览 ({title: *}) {department: w} {name: w} 学号: {id: d}')

    pattern = re.compile(test, re.UNICODE)
    match = pattern.search(u'第7次课-陈子杭-信安3班-2010302530073')
    if match:
        for item in match.groups():
            print item



