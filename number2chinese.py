# -*- coding: utf-8 -*-

chinese_number = [u'零', u'一',u'二',u'三',u'四',u'五',u'六',u'七',u'八',u'九']
ceil_chinese_unit = [u'个',u'十',u'百',u'千']
group_chinese_unit = [u'个', u'万', u'亿']


def translate_number(n):
    chinese_n = ''
    n = str(n)
    if len(n) > 9:
        print u"不支持9位数以上的转换"
        return
    number_groups = {}
    k = 0
    for i in range(len(n), 0, -4):
        j = i-4 if i-4>0 else 0
        number_groups[k] = n[j:i]
        k += 1
    for key, value in number_groups.items():
        sub_number = translate_sub_number(key, value)
        if sub_number.endswith(u'零') and chinese_n.startswith(u'零'):
            sub_number = sub_number.rstrip(u'零')
        chinese_n = sub_number + chinese_n
    chinese_n = chinese_n.rstrip(u'零')
    return chinese_n

def translate_sub_number(key, value):
    group_unit = group_chinese_unit[key]

    len_value = len(value)
    value = value.lstrip('0')
    if not value: return u'零'
    sub_number = ''
    for i in range(len(value)-1, -1, -1):
        c, u = '', ''
        c = chinese_number[int(value[i])]
        if c != u'零' and i != (len(value)-1):
            u = ceil_chinese_unit[len(value)-i-1]
        if c == u'零' and sub_number.startswith(u'零'):
            sub_number = c+u+sub_number.lstrip(u'零')
        else:
            sub_number = c+u+sub_number
    if key > 0 and sub_number.endswith(u'零'):
        sub_number = sub_number.rstrip(u'零')+group_unit+u'零'
    else:
        sub_number = sub_number.rstrip(u'零')+group_unit
    if len(value) < len_value:
        sub_number = u'零' + sub_number
    return sub_number

if __name__ == "__main__":
    print "请输入要转换的数字,-1结束\n"
    while True:
        n = raw_input()
        if n == '-1': 
            break
        chinese_n = translate_number(n)
        print n, '=', chinese_n
