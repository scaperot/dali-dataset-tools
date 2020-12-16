import matplotlib.pyplot as plt
import numpy as np
import os,time

import pdb
import DALI as dali_code
from DALI import utilities

import re
import dali_helpers


if __name__ == '__main__':
    sr = 22050

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()

    allsongfilenames = utilities.get_files_path(dali_path,'.gz')
    delta = []
    song_id = ''
    n = len(allsongfilenames)
    start = time.time()
    lang = []
    print('Collecting the DALI alphabet.')
    for j in range(n):
        #import song metadata
        song_id =  os.path.relpath(allsongfilenames[j],dali_path).split('.')[0]
        dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
        entry = dali_data[song_id]

        #get all lines of song
        lang.append(entry.info['metadata']['language'])

    
    terminate = time.time()
    alphabet.sort()

    print('alphabet for DALI is (',len(alphabet),'): ',''.join(alphabet),)
    print('time to process',n,'songs:',terminate-start)

    np.save('dali_alphabet.npy',''.join(alphabet))
