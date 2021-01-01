
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,librosa
import argparse,subprocess

import DALI as dali_code
from DALI import utilities

import dali_helpers

import nemo_helpers
'''
1. take a .json nemo manifest, find the song ids
2. take those song id's and select 10 songs randomly
3. then create a new manifest with the songs selected
'''
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-o','--old-filename', required=False,type=str,default='dali.json',
                  help='filename for old audio manifest,  Default: dali.json')
    parser.add_argument('-n','--new-filename', required=False,type=str,default='dali.json',
                  help='filename for new audio manifest,  Default: dali.json')
    parser.add_argument('--simple', required=False,default=False,action='store_true',
                  help='simplified hack that only creates the audio manifest from training crops. doesnt download songs or write out wordonset.txt files.')

    args = parser.parse_args()
    filename = args.old_filename
    if not (filename[-5:]=='.json'):
        print('old file must be a .json file',filename)
        sys.exit()

    new_filename = args.new_filename
    if not (new_filename[-5:]=='.json'):
        print('new file must be a .json file',new_filename)
        sys.exit()

    if not os.path.exists(filename):
        print(filename,'does not exist. Try again.')
        sys.exit()

    songids = nemo_helpers.scrap_old_manifest_for_song_id(filename)
    print('Found:',len(songids),'song ids.')
    
    dali_path, audio_path, dali_info = dali_helpers.dali_setup()
    ndxs = np.random.randint(len(songids),size=10)
    
    print('saving new manifest as',args.new_filename)
    for ndx in ndxs:
        song_id = songids[ndx]
        audio_filename = audio_path+'/'+song_id+'.wav'

        # if simple flag is set, do not download song and create wordonset files
        if not args.simple:
            #get song
            if not os.path.exists(audio_filename):
                dali_helpers.download_song(song_id, dali_info, audio_path, 22050)
            else:
                print('skipping download')
            
            # append to .wordonset.txt
            timing_list = dali_helpers.get_onset_timing(song_id)
            nemo_helpers.append_timing(audio_filename,timing_list)
        

        # append to audio manifest
        transcript = dali_helpers.get_full_transcript(song_id)
        nemo_helpers.append_transcript_nemo(args.new_filename,audio_filename,0,transcript)
