import matplotlib.pyplot as plt
import numpy as np
import os,time,sys

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                            filename='./analysis/line_lengths.log',
                            filemode='w',
                            level=logging.INFO)

def line_length_hist_secs(data):
    mu = np.mean(data)
    var = np.var(data)
    std = np.std(data)
    lmin = np.min(data)
    lmax = np.max(data)
    counts,bins = np.histogram(data)
    span = (np.min(data),np.max(data))
    nbins = span[1] - span[0]

    ten_sec_thresh  = 1 - (data.shape[0]-np.where( data < 10 )[0].shape[0] ) / data.shape[0]
    five_sec_thresh  = 1 - (data.shape[0]-np.where( data < 5 )[0].shape[0] ) / data.shape[0]

    title = "DALI Line Lengths: E[X] = %.2f,  min=%.2f, max=%.2f\nLines below 10s: %.1f %%, Lines below 5s: %.1f %%" % (mu, lmin, lmax,ten_sec_thresh*100,five_sec_thresh*100)
    plt.title(title,fontsize=10)
    plt.xlabel('Line Lengths (s)',fontsize=10)
    plt.hist(data,bins=int(nbins),density=True,range=(0,20))
    plt.show(block=True)

if __name__ == '__main__':
    sr = 22050

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()


    # ###############################################
    #

    #  max line length for 5358 songs: 700.2 secs
    #  number of lines above 10 seconds: 605
    #  time to process 5358 songs: 215.2 secs
    #
    # ###############################################
    allsongfilenames = utilities.get_files_path(dali_path,'.gz')
    delta = []
    song_id = ''
    n = len(allsongfilenames)
    print("Measure the length of lines for",n,"songs...")

    # setup toolbar
    toolbar_width = 40
    modulo_val = np.floor(n/toolbar_width).astype(int)
    sys.stdout.write("[%s]" % (" " * (toolbar_width+1)))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+2)) # return to start of line, after '['

    start = time.time()
    neg_length_count = 0
    zero_length_count = 0
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
            tmp = lines[j][1] - lines[j][0]
            #skip lines where the time is less than zero.
            if tmp > 0:
                delta.append(tmp)
            elif tmp == 0:
                zero_length_count += 1
            else:
                neg_length_count += 1
                logging.info('NEGATIVE LINE LENGTH: DALI ID: %s, index (from get_file_path): %d, text: %s, line length: %.2f, line number: %d',song_id,i,annot[j]['text'],tmp / sr,j)
            
            if int(tmp / sr) > 500:
                #find song outlier and investigate
                logging.info('LONG LINE LENGTH: DALI ID: %s, index (from get_file_path): %d, text: %s, line length: %.2f, line number: %d',song_id,i,annot[j]['text'],tmp / sr,j)
        
        if not (i % modulo_val):
            print('-',end='',flush=True)
    print('')

    done = time.time()
    delta = np.array(delta)/sr
    print('max line length for',delta.shape[0],' lines:',np.max(delta))
    print('number of lines above 10 seconds:',np.sum(delta > 10))
    print('time to process',n,'songs:',done-start)
    print('Number of lines reported negative length time:',neg_length_count)
    print('Number of lines reported zero length time:',zero_length_count)


    # plot histogram of values.
    plt.figure(2)
    line_length_hist_secs(delta)

    np.save('./analysis/dali_line_lengths_histogram.npy',delta)
