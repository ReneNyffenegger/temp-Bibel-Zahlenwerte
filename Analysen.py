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

def words_and_letters_in_book(b): #_{
   cnt_words   = 0
   cnt_letters = 0

   letter_counter = {}

   for r in wlc.execute('select word from word_v where b = ?', (b,)):

       word = replace_nikkud(r[0])
       if len(word) and word != 'פ' and word != 'ס':
           cnt_words   += 1
           cnt_letters += len(word)

           for c in word:
               letter_counter[c] = letter_counter.get(c, 0) + 1

   print('{:s} has {:d} words and {:d} letters.'.format(b, cnt_words, cnt_letters))
   for letter in sorted(letter_counter):
       print('  {:s}: {:5d}'.format(letter, letter_counter[letter]))
#_}  

def words_and_letters_in_books():
    words_and_letters_in_book('1mo')
    words_and_letters_in_book('2mo')
    words_and_letters_in_book('3mo')
    words_and_letters_in_book('4mo')
    words_and_letters_in_book('5mo')

def tests(): #_{

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
            
    #_}

    def val_600000(): #_{
#       last_v = 1
        tot_val = 0
        for r in wlc.execute('select word, c, v from word_v where b = "1mo" order by order_'):

            word = replace_nikkud(r[0])
            if len(word) and word != 'פ' and word != 'ס':

#              if r[2] != last_v:
#                 print('')
#                 last_v = r[2]

               tot_val += numeric_value(word)

#              print("{:6d} {:2d}:{:2d} {:s}".format(tot_val, r[1], r[2], word))

               if tot_val > 600000:
                  raise Exception('tot_vat {:d} > 600000'.format(tot_val))

               if tot_val == 600000:
                  if r[1] != 7:
                     raise Exception('chapter: {:d}'.format(r[1]))

                  if r[2] != 24:
                     raise Exception('verse: {:d}'.format(r[2]))

                  if word != 'יום':
                     raise Exception('word is not jam')

                  print('ok tot val 600000')
                  return
                   
    #_}

    test_1mo_1_1()
    letter_86()
    val_600000()

#_}

init()
tests()
words_and_letters_in_books()
