import matplotlib.pyplot as plt
import numpy as np
import os,time,locale

import pdb
import DALI as dali_code
from DALI import utilities

import re
import dali_helpers

def create_histogram(lang):
    #plt.hist(lang)

    total = len(lang)
    total_str = locale.format("%d", total, grouping=True)
    l,counts = np.unique(lang,return_counts=True)
    ndx = np.argmax(np.char.find(l,'english'))
    eng_perc = counts[ndx] / total
    nlangs = len(l)


    title = 'DALI Annotated Languages as a Percentage of Songs \n%s songs, %d lanaguages' % (total_str,nlangs)
    plt.xlabel('DALI Annotated Languages',fontsize=18)
    plt.bar(l,counts/total,color='black')
    plt.xticks(fontsize=16,rotation=90)
    plt.title(title,fontsize=18)
    plt.show()

    #this is what I run on the command line to test out the histogram to avoid running the code below again.
    #its late stop judging me.
    #import numpy as np
    #import dali_language_count
    #data = np.load('./analysis/dali_languages.npy',allow_pickle=True)
    #d = list(data)
    #dali_language_count.create_histogram(d)



if __name__ == '__main__':
    sr = 22050

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()

    allsongfilenames = utilities.get_files_path(dali_path,'.gz')
    delta = []
    song_id = ''
    n = len(allsongfilenames)
    start = time.time()
    lang = []
    print('Collecting the DALI annotated languages.')
    for j in range(n):
        #import song metadata
        song_id =  os.path.relpath(allsongfilenames[j],dali_path).split('.')[0]
        dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
        entry = dali_data[song_id]

        #get all lines of song
        lang.append(entry.info['metadata']['language'])
        print(j,end='\r',flush=True) #print the song number without going to the next line.

    
    terminate = time.time()
    #alphabet.sort()

    #print('alphabet for DALI is (',len(alphabet),'): ',''.join(alphabet),)
    print('time to process',n,'songs:',terminate-start)

    np.save('./analysis/dali_languages.npy',lang)
    create_histogram(lang)
