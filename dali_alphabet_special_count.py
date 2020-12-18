import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,re

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers

less_common_special_alphabet=['"', '#', '$', '%', '&', '(', ')', '*', '+', '/', ':', ';', '<', '=', '>', '@', '[', ']', '^', '_', '`','{', '}']

import logging
logging.basicConfig(format='%(message)s',
                            filename='./analysis/dali_alphabet_special_chars_songs.txt',
                            filemode='w',
                            level=logging.INFO)

def char_exists(input_str):
    '''
    check to see if there is a special character in the string.
    1. char.find - looks at string and reports the highest index 
                   in input_str.  returns the size of special_alphabet.
                   returns -1 for an index if the there is not a numeric
                   character of that type.
    2. max - look for anything that is above -1 which indicates that a 
             char is present.

    Input:
    input_str (string) - string under evaluation.

    Return:
    True/False
    '''
    return (np.max(np.char.find(input_str,less_common_special_alphabet)) >= 0)

if __name__ == '__main__':
    sr = 22050

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()

    allsongfilenames = utilities.get_files_path(dali_path,'.gz')
    delta = []
    song_id = ''
    n = len(allsongfilenames)
    start = time.time()
    alphabet = []
    full_alphabet = []
    songs_with_numbers = []
    print('Looking for DALI songs with special characters in the lyrics.')

    logging.info('DALI Song ID, DALI Song Index (from get_file_path), Line Number, Lyrics')
    song_count = 0
    for j in range(n):
        song_flag = 0
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

        # go through each line and find unique characters and add them
        # to the alphabet
        for i in range(len(text)):
            #add characters to alphabet, then remove duplicates
            if char_exists(text[i]):
                logging.info('%s, %d, %d, %s, %s',song_id,j,i,entry.info['metadata']['language'],annot[i]['text'])
                song_flag = 1

        if song_flag:
            song_flag = 0
            song_count += 1
        print(j,end='\r',flush=True) #print the song number without going to the next line.


    terminate = time.time()
    alphabet.sort()

    print('songs with special characters for DALI is):',song_count)
    logging.info('Songs with special characters for DALI is: %d',song_count)

    print('time to process',j,'songs:',terminate-start)

