
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,librosa
import argparse,subprocess

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers
import nemo_helpers

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='calculate all windows based on 10.2268s window with a step thats half the size, find the words for a DALI generated transcript for song ID 3698c37beab64ec39196875d69720822 (assuming that songs are already in audio/ directory.')
    parser.add_argument('-s','--song-id', required=False,type=str,default='',
            help='DALI song id.  default: '', example: 3698c37beab64ec39196875d69720822' )
    
    args = parser.parse_args()

    #required inputs
    sample_rate = int(22050.0)
    win_samples = int(10.2268 * sample_rate)

    if args.song_id == '':
        song_id = '3698c37beab64ec39196875d69720822'  #this may not exist...
    else:
        song_id = args.song_id

    #setup DALI 
    dali_path, audio_path, dali_info = dali_helpers.dali_setup()
    x,sr = librosa.load(audio_path+'/'+song_id+'.wav')

    #import song metadata
    dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
    dali_entry = dali_data[song_id]
    dali_annot = dali_entry.annotations['annot']

    #calcuate indices...by importing from audio/
    song_ndx = dali_helpers.calc_window_for_song(x.shape[0],win_samples)
    #song_ndx = np.load(audio_path+'/'+song_id+'_crop_indices.npy')


    tstart = time.time()
  
    tlist,timing_list = dali_helpers.get_cropped_transcripts(song_id,dali_annot,song_ndx,sample_rate)

    tend = time.time()
    print('Time to process one song:',tend-tstart)

    print('Write word onset timing to audio/')
    # save all cropped files in nemo format
    for i in range(len(timing_list)):
        i_str = str(i).zfill(3)
        nemo_helpers.append_timing('audio/'+song_id+'_'+i_str+'.wav',timing_list[i])
    ncrops = song_ndx.shape[0]
    k = np.random.randint(ncrops)
    k_str = str(k).zfill(3)

    for i in range(len(tlist)):
        print('selected segment:',k,', segment:',i,', transcript:',tlist[i])
    
    #if song is in the audio directory, play it.
    #filename  = 'audio/'+song_id + '_'+k_str+'.wav'
    #subprocess.call(['aplay', filename])




