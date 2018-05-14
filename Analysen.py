#!/usr/bin/python
# vi: foldmethod=marker foldmarker=_{,_}
# -*- coding: utf-8 -*-

import sqlite3
import os
import re

def open_db(): #_{

    global wlc, BP5, wrd

    wlc_path = os.environ['github_root'] + 'Bible-Text-Sources/github.openscriptures/wlc.db'
    BP5_path = os.environ['github_root'] + 'Bible-Text-Sources/github.byztxt/BP5.db'
    wrd_path = os.environ['github_root'] + 'Bible-Text-Sources/strongs/strongs.db'
    
    if not os.path.isfile(wlc_path):
       raise Exception(wlc_path + ' not found')
    
    if not os.path.isfile(BP5_path):
       raise Exception(BP5_path + ' not found')

    if not os.path.isfile(wrd_path):
       raise Exception(srd_path + ' not found')
    
    wlc = sqlite3.connect(wlc_path).cursor()
    PB5 = sqlite3.connect(BP5_path).cursor()
    wrd = sqlite3.connect(wrd_path).cursor()
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
       'ת' : 400,
       'Α' :   1,
       'Ἀ' :   1,
       'α' :   1,
       'ἀ' :   1,
       'Β' :   2,
       'β' :   2,
       'Γ' :   3,
       'γ' :   3,
       'Δ' :   4,
       'δ' :   4,
       'Ε' :   5,
       'ε' :   5,
       'ἐ' :   5,
       'Ζ' :   7,
       'ζ' :   7,
       'Η' :   8,
       'η' :   8,
       'ή' :   8,
       'ἡ' :   8,
       'θ' :   9,
       'Θ' :   9,
       'Ι' :  10,
       'ι' :  10,
       'ΐ' :  10,
       'Κ' :  20,
       'κ' :  20,
       'Λ' :  30,
       'λ' :  30,
       'Μ' :  40,
       'μ' :  40,
       'Ν' :  50,
       'ν' :  50,
       'Ξ' :  60,
       'ξ' :  60,
       'Ο' :  70,
       'ο' :  70,
       'Π' :  80,
       'π' :  80,
       'Ϟ' :  90,
       'ϟ' :  90,
       'Ρ' : 100,
       'Ῥ' : 100,
       'ρ' : 100,
       'Σ' : 200,
       'Τ' : 300,
       'Υ' : 400,
       'ϋ' : 400,
       'ῦ' : 400,
       'Φ' : 500,
       'Χ' : 600,
       'Ψ' : 700,
       'Ω' : 800,
       'ς' : 200,
       'σ' : 200,
       'τ' : 300,
       'υ' : 400,
       'φ' : 500,
       'χ' : 600,
       'ψ' : 700,
       'Ὧ' : 800,
       'ω' : 800,
       'ῶ' : 800,
       'ώ' : 800,
       'Ϡ' : 900,
       'ϡ' : 900,
       'ἱ' :  10,
       'Ἰ' :  10,
       'ὰ' :   1,
       'ά' :   1,
       'ί' :  10,
       'ὸ' :  70,
       'ᾶ' :   1,
       'ῆ' :   8,
       'ῖ' :  10,
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
        try:
           v = v + num_values[c]
        except KeyError:
           print('KeyError in word {:s}, character {:s}'.format(txt, c))
           raise

    return v
#_}        

def numeric_value_translation(word_de, lang): #_{

    for r in wrd.execute('select word from strongs where lang = ? and word_de = ?', (lang, word_de)):
        word = replace_nikkud(r[0])
        return numeric_value(word)


#_}

def numeric_value_verse(db, b, c, v): #_{
    val_tot = 0
    for r in db.execute('select word from word_v where b = ? and c = ? and v = ? order by order_', (b, c, v)):

        word = replace_nikkud(r[0])

        if len(word) and word != 'פ' and word != 'ס':
           val_word = numeric_value(word)
#          print(' {:d} : {:4d}'.format(len(word), val_word))
           val_tot = val_tot + val_word

    return val_tot

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

def words_and_letters_in_books(): #_{
    words_and_letters_in_book('1mo')
    words_and_letters_in_book('2mo')
    words_and_letters_in_book('3mo')
    words_and_letters_in_book('4mo')
    words_and_letters_in_book('5mo')
#_}

def twelve_tribes(): #_{
    tot_val = 0
    for name in ['Juda', 'Ruben', 'Gad', 'Asser', 'Naphtali', 'Manasse', 'Simeon', 'Levi', 'Issaschar', 'Sebulon', 'Joseph', 'Benjamin']: # Revelation 7:5 ff
    # 'Ruben', 'Simeon', 'Levi', 'Juda', 'Dan', 'Naphtali', 'Gad', 'Asser', 'Issaschar', 'Sebulon', 'Joseph', 'Benjamin'
        val = numeric_value_translation(name, 'G')
        tot_val += val
        print('{:10s} {:4d}'.format(name, val))

    tot_val += 200 # Add missing σ in Ἰσσαχάρ (?)
    print('{:10s} {:4d}'.format('Total', tot_val))

    print('')

    tot_val = 0
    for name in ['Ruben', 'Simeon', 'Levi', 'Juda', 'Dan', 'Naphtali', 'Gad', 'Asser', 'Issaschar', 'Sebulon', 'Joseph', 'Benjamin']: # Direct sons
        val = numeric_value_translation(name, 'H')
        tot_val += val
        print('{:10s} {:4d}'.format(name, val))
    print('{:10s} {:4d}   {:s}  {:4d}'.format('Total', tot_val, '= 37*86', 37*86))

    print('')

    tot_val = 0
    for name in ['Ruben', 'Simeon', 'Juda', 'Dan', 'Naphtali', 'Gad', 'Asser', 'Issaschar', 'Sebulon', 'Benjamin', 'Ephraim', 'Manasse']: # Without Levi and Josef, but with Ephraim and Manassse 
        val = numeric_value_translation(name, 'H')
        tot_val += val
        print('{:10s} {:4d}'.format(name, val))
    tot_val -= 6 # The first occurence of Sebulon is spelled זְבֻלֽוּן (missing wav). Subtracting it.
    print('{:10s} {:4d}'.format('Total', tot_val))

#_}

def n2701(): #_{

    val_1mo_8_14 = numeric_value_verse(wlc, '1mo', 8, 14)
    print('Value of 1. Mo 8:14 is {:d}'.format(val_1mo_8_14))

#_}

def tests(): #_{

    def test_1mo_1_1(): #_{

        val_1mo_1_1 = numeric_value_verse(wlc, '1mo', 1, 1)

        if val_1mo_1_1 != 2701:
           raise Exception('1. Mo 1:1, val_tot is {:d}'.format(val_1mo_1_1))

        print('ok Total value 1. Mo 1:1 is {:d}'.format(val_1mo_1_1))

    #_}

    def letter_86(): #_{ 86th letter starts word אלהים

        letter_no = 1
        for r in wlc.execute('select word from word_v where b = "1mo" order by order_'):
            word = replace_nikkud(r[0])
            if len(word) and word != 'פ' and word != 'ס':

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

    def test_numeric_value_translation(): #_{

        val_noah = numeric_value_translation('Noah', 'H')
        if val_noah != 58:
           raise Exception('Value of Noah: {:d}'.format(val_noah))
        
        print('ok Value Noah')

        val_juda = numeric_value_translation('Juda', 'G')
        if val_juda != 485:
           raise Exception('Value of Juda: {:d}'.format(val_juda))
        
        print('ok Value Juda')


    #_}

    test_1mo_1_1()
    test_numeric_value_translation()
    letter_86()
    val_600000()

#_}

init()
tests()
# words_and_letters_in_books()
# twelve_tribes()
n2701()
