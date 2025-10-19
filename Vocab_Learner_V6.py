#!/usr/bin/python
print("------------ Vocab_Learner -----------")
print('Loading dependencies ...')

import os, sys, csv, re, linecache, nltk, time
from nltk.corpus import brown
from datetime import date
from unidecode import unidecode
import keyboard

# Intro------------------------------------------------------------
# NLTK
# NLTK is used to automatically categorize the words you input.
# You may have to download several dictionaries such as nltk.download('universal_tagset').
# NLTK will prompt you to download what is missing.

# Open google translate in Opera as helpful tool
import webbrowser
url1 = 'https://translate.google.com/?sl=mn&tl=en&op=translate'
url2 = 'https://bolor-toli.com'
opera_path = 'C:/Users/Leo Rauschenberger/AppData/Local/Programs/Opera/opera.exe %s --incognito'
webbrowser.get(opera_path).open_new(url1)
webbrowser.get(opera_path).open_new_tab(url2)


# Language code
# You can save words of several languages in the list. Use a one-letter code (such as C = Chinese) to easily access them:
langlist=['C','F','M','V']

# .csv-File containing your dictionary (If it doesn't exist yet, the program will create it):
folderloc = "C:/Users/Leo Rauschenberger/Desktop/Program&Design/"
name = "vocab_list_V4.csv"
filename = folderloc+name

# Functions
def findword(word,cn):
    with open(filename,"r",encoding="utf-8") as filex:
        reader = csv.reader(filex, delimiter="\t")
        for row in reader:
            rowlist = re.split(',', row[0])
            # case insensitive string matching ( casefold converts S to s and ß to ss )
            if word.casefold() in (item.casefold() for item in rowlist):
                cn = cn + 1
                print(cn,'\t'.join(rowlist))
        return cn

# resolve issues with displaying some Mongolian letters
def barred_o():
    keyboard.send('backspace')
    keyboard.write('ө')
def big_barred_o():
    keyboard.send('backspace')
    keyboard.write('Ө')
def straight_y():
    keyboard.send('backspace')
    keyboard.write('ү')
def big_straight_y():
    keyboard.send('backspace')
    keyboard.write('Ү')
keybrd = 'eng'
if keybrd == 'mng':
    keyboard.add_hotkey('ө', barred_o)
    keyboard.add_hotkey('shift+ө', big_barred_o)
    keyboard.add_hotkey('ү', straight_y)
    keyboard.add_hotkey('shift+ү', big_straight_y)
# ------------------------------------------------------------

# Load file. If file doesn't exist add it.
print("Loading",filename)
if not os.path.exists(filename):
    with open(filename, "a") as file:
        file.write("Lang\tOrig.Lang\tDecoded\tEnglish\tType\tDate\tComments\n--------------------------------------------------------------------------------------------------------------------------\n")

# Tell userb when it was last updated
#last_modified_time = os.path.getmtime(filename)
#readable_time = datetime.fromtimestamp(last_modified_time)
#print('Last update to file: ',readable_time)

# open the file
csv_file = csv.reader(open(filename, "r"), delimiter="\t")

# -----------------------------------------------------------
run = 'y'
while run == 'y':
    choice = ''
    while choice not in ['1','2']:
        choice = input("Enter (1) Lookup or (2) New word entry: ")

    # ---- Look up word ------
    if choice == '1':
        cntr = 0 # resetting results counter
        myword = input("Enter word/language code/word type you want to find (Enter shows all): ")
        cntr = findword(myword, cntr)
        print('Matches:',cntr)
        # if no results were found:
        if cntr == 0:print(" -------- Sorry, no entry found. Please enter it now. --------")

    # ---- Add word -----
    if choice == '2' or cntr == 0:
        # Since multiple languages can be stored in the same list, 'lang_code' is used
        lang_code = ''
        while lang_code not in langlist: 
            lang_code = input("Enter Language Code (M, C, ...): ").upper()
            if lang_code not in langlist:
                answer = input("Unknown code. To try again, press enter. To add a NEW language, please enter the same code again: ").upper()
                if answer == lang_code and len(answer)>0:
                    langlist.append(lang_code)
                    print("Code added, new list: ",langlist)
        entry_fl = input("Word in Foreign Language ------: ")
        entry_en = input("Word in English Language ------: ")
        notes = input("Add example sentence or comment: ")

        decoded = unidecode(entry_fl)

        #worddist = nltk.FreqDist(t for w, t in brown.tagged_words() if w.lower() == entry_en)
        worddist = nltk.FreqDist(t for w, t in brown.tagged_words(tagset='universal') if w.lower() == entry_en)
        try:
            wordcl = worddist.most_common()[0][0]  # checks for most common usage
        except:
            print('Auto-tagging class had no matches.')
            wordcl = input("Please input class yourself (NOUN, ADV, ADJ, VERB, ...): ")
        
        # print(wordcl)

        lstitem =[lang_code, entry_fl, decoded, entry_en, wordcl, str(date.today()), notes]
        print(lstitem)

        with open(filename,'a',encoding='utf8') as file:
            for item in lstitem:
                file.write(item+",")
            file.write("\n")

        print("Input added.")
        file.close()

    run = ''
    while run not in ['y','n']: 
        run = input('Next word? y/n: ').lower()

print("Exiting script.")
time.sleep(2)
