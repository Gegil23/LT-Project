import FrequencySummarizer
from heapq import nlargest
from shutil import copy, rmtree
from random import shuffle
import glob
import os


POLITICS = os.getcwd() + "\\bbc\\politics"
SPORTS = os.getcwd() + "\\bbc\\sport"
TECH = os.getcwd() + "\\bbc\\tech"

def summarise(filename, n=3):

    fs = FrequencySummarizer.FrequencySummarizer()
    file = open(filename, "r").read()
    old_text = file.split("\n")[1:]
    text = list(filter(lambda a: a != '', old_text))
    if len(text) >= n:    
        relevant = {}
        dic = {}
  
        for p in text:
            summary = fs.summarize(p,1)
            sentence, rank = summary[0]
            dic[text.index(p)] = sentence
            relevant[text.index(p)] = rank
    
        rel_ind = nlargest(n, relevant, key=relevant.get)
        p_summ = ""
        for i in sorted(rel_ind):
            p_summ += dic[i] + '\n'
        return p_summ
    else:
        summary = fs.summarize(" ".join(text),n)
        p_summ = ""
        for s in summary:
            p_summ += s[0]
        return p_summ

def choose_radomised_texts(folder_path, folder_destination, n=6):
    rmtree(folder_destination)
    os.makedirs(os.getcwd() + '\\' + folder_destination)
    filenames = glob.glob(folder_path + "/*.txt")
    shuffle(filenames)
    for text in filenames[:6]:
        copy(text, folder_destination)

def G3(folder):
    filenames = glob.glob(folder + "/*.txt")[:6]
    #filename = folder + '/' + folder + '.txt'

    for text in filenames:
        filename = folder + '\\' + "summary_G3_" + text[-7:]
        file = open(filename, 'w')
        summary = summarise(text, 3)
        file.write(text + '\n')
        file.write(summary)
        file.write('\n\n')
    file.close()

def G3_1(folder):
    filenames = glob.glob(folder + "/*.txt")[:6]
    filename = folder + '/' + folder + '.txt'
    file = open(filename, 'w')

    for text in filenames:
        summary = summarise(text, 3)
        file.write(text + '\n')
        file.write(summary)
        file.write('\n\n')
    file.close()




#choose_radomised_texts(POLITICS, "politics")
#choose_radomised_texts(TECH, "tech")
#choose_radomised_texts(SPORTS, "sport")

#G3_1("politics")
#G3_1("tech")
#G3_1("sport")

G3("politics")
G3("tech")
G3("sport")