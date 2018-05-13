#!/usr/bin/python
# vi: foldmethod=marker foldmarker=_{,_}

import sqlite3
import os
import re



def open_db(): #_{

    global wlc, BP5_path

    wlc_path = os.environ['github_root'] + 'Bible-Text-Sources/github.openscriptures/wlc.db'
    BP5_path = os.environ['github_root'] + 'Bible-Text-Sources/github.byztxt/BP5.db'
    
    if not os.path.isfile(wlc_path):
       raise Exception(wlc_path + ' not found')
    
    if not os.path.isfile(BP5_path):
       raise Exception(BP5_path + ' not found')
    
    wlc = sqlite3.connect(wlc_path).cursor()
    PB5 = sqlite3.connect(BP5_path).cursor()
#_}

def init_num_values(): #_{

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
       'ת' : 400 
    }
#_}

def init(): #_{
    open_db()
    init_num_values()
#_}

def replace_nikkud(txt): #_{

    txt = txt.replace('/', '') # Temporarily replace slashes, too.

    return re.sub('[\u0591-\u05C7]', '', txt)
#_}

def numeric_value(txt): #_{

    v = 0
    for c in txt:
        v = v + num_values[c]

    return v
#_}        

def tests():

    def test_1mo_1_1(): #_{

        val_tot = 0
        for r in wlc.execute('select word from word_v where b = "1mo" and c = "1" and v = "1" order by order_'):

            word = replace_nikkud(r[0])


            if len(word):
               val_word = numeric_value(word)
        #      print(' {:d} : {:4d}'.format(len(word), val_word))
               val_tot = val_tot + val_word

        if val_tot != 2701:
           raise Exception('1. Mo 1:1, val_tot is {:d}'.format(val_tot))

        print('ok Total value 1. Mo 1:1 is {:d}'.format(val_tot))

    #_}

    def letter_86(): #_{ 86th letter starts word אלהים

        letter_no = 1
        for r in wlc.execute('select word from word_v where b = "1mo" order by order_'):
            word = replace_nikkud(r[0])
            if len(word):

            #  print("{:2d} {:s}".format(letter_no, word))

               if letter_no > 100:
                  raise Exception('Letter is {:d}'.format(letter_no))

               if letter_no == 86:
                  if word != 'אלהים':
                     raise Exception('86th does not start word Elohim')

                  print('ok 86th letter starts word Elohim')
                  return

               letter_no += len(word)
            

    test_1mo_1_1()
    letter_86()

init()
tests()
