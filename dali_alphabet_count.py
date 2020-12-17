import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,re

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers


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

    print('Collecting the DALI alphabet.')

    # setup toolbar
    toolbar_width = 40
    modulo_val = np.floor(n/toolbar_width).astype(int)
    sys.stdout.write("[%s]" % (" " * (toolbar_width+1)))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+2)) # return to start of line, after '['

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

        # go through each line and find unique characters and add them
        # to the alphabet
        for i in range(len(text)):
            #add characters to alphabet, then remove duplicates
            alphabet.extend(text[i])
            alphabet = list(set(alphabet))
        #print(j,end='\r',flush=True) #print the song number without going to the next line.

        if not (i % modulo_val):
            print('-',end='',flush=True)
    print('')

    terminate = time.time()
    alphabet.sort()

    print('alphabet for DALI is (',len(alphabet),'): ',''.join(alphabet),)
    print('time to process',i,'songs:',terminate-start)

    np.save('./analysis/dali_alphabet.npy',''.join(alphabet))
