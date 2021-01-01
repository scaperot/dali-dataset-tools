
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,librosa
import argparse,subprocess

import DALI as dali_code
from DALI import utilities

import dali_helpers


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='given a time window, attempt to find the characters for a DALI generated transcript')
    parser.add_argument('-f','--filename', required=False,type=str,default='/blah/3698c37beab64ec39196875d69720822.wav',
                  help='DALI song id.  Default: /blah/3698c37beab64ec39196875d69720822.wav, ')

    args = parser.parse_args()


    #required inputs
    filename_raw = args.filename

    filename = filename_raw.split('/')[-1]

    #setup DALI 
    if not os.path.exists(filename_raw):
        print(filename_raw,'does not exist.  Try downloading the song (if you need it!).')

    transcript = dali_helpers.get_full_transcript_by_filename(filename)
    song_id = filename.split('.')[0]

    print('song id:',song_id,', transcript:',transcript)

