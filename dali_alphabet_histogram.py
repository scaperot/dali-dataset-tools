import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,re,locale

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers

numeric_alphabet=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
special_alphabet=['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`','{', '}']
special_alphabet_replacement_candidates=['#', '$', '%', '&', '(', ')', '*', '+', '/','<', '=', '>', '?', '@', '[', ']', '^', '_', '`','{', '}']
standard_alphabet = [' ', "'",'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#wikipedia reference for letter frequency for English
english_alphabet_frequency = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]

def initialize_histogram_dict(alphabet,alphabet_dict):
    '''


    Input:
    alphabet (string): all characters in DALI dataset found by 

    Return:
    N/A (pass by reference)
    '''
    #break into list
    clist = list(alphabet)
    for c in range(len(clist)):
        alphabet_dict[clist[c]] = 0
    

    '''
    create three subplots.

    1. targeted alphabet (alphabet characters, spaces, apostrophe)
    2. numbers           
    3. special characters

    title: group counts out of total counts (% of total)
    plot:  group counts

    '''
def histogram(alphabet_dict):
    '''
    '''
    chars = list(alphabet_dict.keys())
    vals  = list(alphabet_dict.values())
    total = np.sum(vals)
    plt.bar(chars,np.log(vals),color='black')
    total_str = locale.format("%d", total, grouping=True)
    title = 'DALI dataset Character makeup (66 total categories)\n Total of %s characters.' % (total_str)
    plt.title(title,fontsize=18)
    plt.xlabel('Dataset Characters',fontsize=18)
    plt.ylabel('Occurances (log scale)',fontsize=18)

    plt.show(block=True)

    #code used to run this function last
    #import numpy as np
    #import dali_alphabet_histogram
    #data = np.load('./analysis/dali_alphabet_histogram.npy',allow_pickle=True)
    #d = data.item()
    #dali_alphabet_histogram.histogram(d)

def categories_test(alphabet_dict):
    '''
    1. targeted alphabet (alphabet characters, spaces, apostrophe)
    2. numbers           
    3. special characters
    '''
    #create histogram of alphabet characters
    s_count = 0
    for c in special_alphabet:
        s_count += alphabet_dict[c]

    a_count = 0
    for c in standard_alphabet:
        a_count += alphabet_dict[c]

    n_count = 0
    for c in numeric_alphabet:
        n_count += alphabet_dict[c]

    total = n_count+a_count+s_count
    size = [n_count,a_count,s_count]
    print(n_count,a_count,s_count)

    #title = "DALI groups of characters: numeric (0-9), special characters, and 28 character set (a-z, apostrophe, and space).\nTotal of %d" % (total)
    #plt.title(title,fontsize=20)
    #plt.pie(size,labels = ['Numeric Characters','28 Character Set','Special Characters'],autopct='%1.4f%%')
    #plt.show(block=True)


if __name__ == '__main__':
    sr = 22050

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()

    allsongfilenames = utilities.get_files_path(dali_path,'.gz')
    delta = []
    song_id = ''
    n = len(allsongfilenames)
    start = time.time()

    print('Collecting the DALI alphabet.')
    required_file = './analysis/dali_alphabet.npy'
    alphabet_count = {}

    #attempt to load the known raw alphabet
    if os.path.isfile(required_file):
        full_alphabet = str(np.load(required_file))
        initialize_histogram_dict(full_alphabet, alphabet_count)
        #print(alphabet_count)
    else:
        print('Need ./analysis/dali_alphabet.npy to run the histogram (you could modify this code to make your own custom dictionary as an alternative).')
        sys.exit()

    for j in range(n):
    #for j in np.arange(1,100):
        #import song metadata
        song_id =  os.path.relpath(allsongfilenames[j],dali_path).split('.')[0]
        dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
        entry = dali_data[song_id]


        #skip non-english songs.
        #if entry.info['metadata']['language'] != 'english':
        #    continue

        #get all lines of song
        annot = entry.annotations['annot']['paragraphs']
        text = []
        text = [j['text'] for j in dali_code.annot2frames(annot,1/sr)]

        # go through each paragraph and add characters to count
        for i in range(len(text)):
            #pdb.set_trace()

            #add characters to alphabet
            # 1. list to make the string into a character array.
            # 2. numpy unique to provide counts and characters
            chars,counts = np.unique(list(text[i]),return_counts=True)
            
            # loop through all characters in paragraph and 
            # add them to the existing alphabet_count
            for c in range(len(chars)):
                alphabet_count[chars[c]] += counts[c]

        print(j,end='\r',flush=True) #print the song number without going to the next line.

    terminate = time.time()

    #print('alphabet for DALI is (',len(alphabet),'): ',''.join(alphabet),)
    print('time to process',j,'songs:',terminate-start)
    np.save('./analysis/dali_alphabet_histogram.npy',alphabet_count)
