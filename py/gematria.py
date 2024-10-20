
import re

nikud_pattern = re.compile(r'[\u0591-\u05C7]')

def remove_nikud(t):
    return nikud_pattern.sub('', t)

def val_letter(l):
    if l == 'א': return   1
    if l == 'ב': return   2
    if l == 'ג': return   3
    if l == 'ד': return   4
    if l == 'ה': return   5
    if l == 'ו': return   6
    if l == 'ז': return   7
    if l == 'ח': return   8
    if l == 'ט': return   9
    if l == 'י': return  10
    if l == 'ך': return  20
    if l == 'כ': return  20
    if l == 'ל': return  30
    if l == 'ם': return  40
    if l == 'מ': return  40
    if l == 'ן': return  50
    if l == 'נ': return  50
    if l == 'ס': return  60
    if l == 'ע': return  70
    if l == 'ף': return  80
    if l == 'פ': return  80
    if l == 'ץ': return  90
    if l == 'צ': return  90
    if l == 'ק': return 100
    if l == 'ר': return 200
    if l == 'ש': return 300
    if l == 'ת': return 400
#   if l == 'תָֽ': return 400
#   if l == 'תֹ': return 400
#   if l == 'תִּ': return 400


def value(t):
    for l in remove_nikud(t):
        print(val_letter(l))

    print('Sum: ' + str(sum( val_letter(l) for l in remove_nikud(t))))






























