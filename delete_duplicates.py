# -*- coding: utf-8 -*- 
a = []

txt = open('text.txt', 'r')
ntxt = open('new_text.txt', 'w')

for row in txt.readlines():
    if row.count('.') >= 2:
        continue
    qb = row.split(' ')
    b = ' '
    for j in qb:
        if len(j) > 1:
            b = b + j + ' '
    print(b, b in a)
    if b not in a:
        a.append(b)
        ntxt.write(b + '\n')