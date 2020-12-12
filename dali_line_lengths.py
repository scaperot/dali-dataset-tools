import matplotlib.pyplot as plt
import numpy as np
import os,time,sys

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers

def line_length_hist_secs(data):
    counts,bins = np.histogram(data)
    span = (np.min(data),np.max(data))
    nbins = span[1] - span[0]
    plt.hist(data,bins=int(nbins),range=(0,20))
    plt.show(block=False)

if __name__ == '__main__':
    sr = 22050

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()


    # ###############################################
    #
    print("Measure the length of lines for all songs...")
    #  max line length for 5358 songs: 700.2 secs
    #  number of lines above 10 seconds: 605
    #  time to process 5358 songs: 215.2 secs
    #
    # ###############################################
    allsongfilenames = utilities.get_files_path(dali_path,'.gz')
    delta = []
    song_id = ''
    n = len(allsongfilenames)

    # setup toolbar
    toolbar_width = 40
    modulo_val = np.floor(n/toolbar_width).astype(int)
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    start = time.time()

    for i in range(n):
        #import song metadata
        song_id =  os.path.relpath(allsongfilenames[i],dali_path).split('.')[0]
        dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
        entry = dali_data[song_id]

        #get all lines of song
        annot = entry.annotations['annot']['lines']
        lines = []
        lines = [i['time'] for i in dali_code.annot2frames(annot,1/sr)]
        nlines = len(lines)

        for j in range(nlines):
            delta.append(lines[j][1] - lines[j][0])
        
        if not (i % modulo_val):
            print('=',end='',flush=True)
    print('')

    done = time.time()
    delta = np.array(delta)/sr
    print('max line length for',n,'songs:',np.max(delta))
    print('number of lines above 10 seconds:',np.sum(delta > 10))
    print('time to process',n,'songs:',done-start)


    # plot histogram of values.
    plt.figure(2)
    line_length_hist_secs(delta)

    np.save('dali_histogram.npy',delta)
