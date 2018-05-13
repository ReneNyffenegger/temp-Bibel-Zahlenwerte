#!/usr/bin/python

import sqlite3
import os
import re



def open_db():

    global wlc, BP5_path

    wlc_path = os.environ['github_root'] + 'Bible-Text-Sources/github.openscriptures/wlc.db'
    BP5_path = os.environ['github_root'] + 'Bible-Text-Sources/github.byztxt/BP5.db'
    
    if not os.path.isfile(wlc_path):
       raise Exception(wlc_path + ' not found')
    
    if not os.path.isfile(BP5_path):
       raise Exception(BP5_path + ' not found')
    
    wlc = sqlite3.connect(wlc_path).cursor()
    PB5 = sqlite3.connect(BP5_path).cursor()

def init_num_values():

    global num_values 
    num_values = {
       'א' :   1,
       'ב' :   2,
       'ג' :   3,
       'ד' :   4,
       'ה' :   5,
       'ו' :   6,
       'ז' :   7,
       'ח' :   8,
       'ט' :   9,
       'י' :  10,
       'ך' :  20,
       'כ' :  20,
       'ל' :  30,
       'ם' :  40,
       'מ' :  40,
       'ן' :  50,
       'נ' :  50,
       'ס' :  60,
       'ע' :  70,
       'ף' :  80,
       'פ' :  80,
       'ץ' :  90,
       'צ' :  90,
       'ק' : 100,
       'ר' : 200,
       'ש' : 300,
       'ת' : 400 }

def init():
    open_db()
    init_num_values()

def replace_nikkud(txt):

    txt = txt.replace('/', '') # Temporarily replace slashes, too.

    return re.sub('[\u0591-\u05C7]', '', txt)

def numeric_value(txt):

    v = 0
    for c in txt:
        v = v + num_values[c]

    return v
        

def tests():

    def test_1mo_1_1():

        val_tot = 0
        for r in wlc.execute('select word from word_v where b = "1mo" and c = "1" and v = "1" order by order_'):

            word = replace_nikkud(r[0])

            val_word = numeric_value(word)

            if len(word):
               print(' {:d} : {:4d}'.format(len(word), val_word))
               val_tot = val_tot + val_word

        print('Total value 1. Mo 1:1 is {:d}'.format(val_tot))

    test_1mo_1_1()

init()
tests()
