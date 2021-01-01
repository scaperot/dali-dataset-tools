
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,argparse

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers




if __name__ == "__main__":

    #parser = argparse.argumentparser(description='print index of possible windows')
    #parser.add_argument('-s','--song-id', required=false,type=str,default='3698c37beab64ec39196875d69720822',
    #        help='dali song id. default: 3698c37beab64ec39196875d69720822')
    #args = parser.parse_args()
    
    total_samples = np.floor(5.3 * 60 * 22050).astype(int) #5 min song
    win_samples   = 225500 #10.23 seconds
    #start_ndx,end_ndx = dali_helpers.calc_window_for_song(total_samples,win_samples) 
    #song_ndx = dali_helpers.calc_window_for_song(total_samples,win_samples) 
    #print(song_ndx.shape)
    #for i in range(song_ndx.shape[0]):
    #    print(song_ndx[i,0].T,song_ndx[i,1])



