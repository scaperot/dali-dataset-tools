
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,librosa
import argparse,subprocess

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='given a time window, attempt to find the characters for a DALI generated transcript')
    parser.add_argument('-i','--index', required=False,type=int,default=5,
                   help='index of crop (overlapping crop pattern) window / song segment relative to the start of the song.')
    parser.add_argument('-w','--window', required=False,type=float,default=10.2268,
                   help='size of window of DALI song, to create a transcript')
    parser.add_argument('-s','--song-id', required=False,type=str,default='3698c37beab64ec39196875d6972082',
                  help='DALI song id.  Default: 3698c37beab64ec39196875d69720822, ')

    args = parser.parse_args()

    #TODO: if audio is not available in audio, download

    #required inputs
    song_id = args.song_id
    x,sr    = librosa.load('audio/'+song_id+'.wav',sr=None)
    window_samples = args.window * sr
    window_index   = args.index
    all_windows_secs = dali_helpers.calc_window_for_song(x.shape[0],window_samples)
    start = all_windows_secs[window_index,0]
    term  = all_windows_secs[window_index,1]
    window_secs  = np.array([start,term]) / sr

    #setup DALI 
    dali_path, audio_path, dali_info = dali_helpers.dali_setup()

    #import song metadata
    dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
    entry = dali_data[song_id]
    annot = entry.annotations['annot']

    transcript,onset_timing, offset= dali_helpers.get_transcript_for_window(song_id,annot, window_secs, window_index)

    print('Song:',song_id,', window:',window_secs, ', transcript:',transcript,',offset:',offset,', timing:',onset_timing)

    #if song is in the audio directory, play it.
    #filename  = audio_path+'/'+song_id + '_01.wav'
    #subprocess.call(['aplay', filename])

