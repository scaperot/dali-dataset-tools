
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,librosa
import argparse,subprocess

import DALI as dali_code
from DALI import utilities

import dali_helpers


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='given a time window, attempt to find the characters for a DALI generated transcript')
    parser.add_argument('-s','--song-id', required=False,type=str,default='3698c37beab64ec39196875d69720822',
                  help='DALI song id.  Default: 3698c37beab64ec39196875d69720822, ')

    args = parser.parse_args()


    #required inputs
    song_id = args.song_id


    #setup DALI 
    dali_path, audio_path, dali_info = dali_helpers.dali_setup()
    song_fname = audio_path+'/'+song_id+'.wav'
    if not os.path.exists(song_fname):
        print(song_fname,'does not exist.  Try downloading the song (if you need it!).')

    transcript = dali_helpers.get_full_transcript(song_id)

    print('Song:',song_id,', transcript:',transcript, ', number of words:',len(transcript.split()))

