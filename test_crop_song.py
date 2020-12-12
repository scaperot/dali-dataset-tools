
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,argparse

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='print a song transcript')
    parser.add_argument('-s','--song-id', required=False,type=str,default='3698c37beab64ec39196875d69720822',
            help='dali song id. default: 3698c37beab64ec39196875d69720822')

    args = parser.parse_args()
    
    dali_path, audio_path, dali_info = dali_helpers.dali_setup()
    
    song_id = args.song_id
    win_samples = 225500
    
    dali_entry = dali_code.get_the_DALI_dataset(dali_path, keep=[song_id])[song_id]

    song_indices, filename_list = dali_helpers.crop_song(song_id, audio_path, dali_entry, win_samples)

    for i in range(len(filename_list)):
        print(filename_list[i],', ',song_indices[i,:])




