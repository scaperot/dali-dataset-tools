
import matplotlib.pyplot as plt
import numpy as np
import os,time,sys,argparse,librosa

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='print a song transcript')
    parser.add_argument('-s','--song-id', required=False,type=str,default='3698c37beab64ec39196875d69720822',
            help='dali song id. default: 3698c37beab64ec39196875d69720822')

    args = parser.parse_args()
    song_id = args.song_id

    x,sr = librosa.load('audio/'+song_id+'.wav')

    xnorm = dali_helpers.normalize_data(x)

    plt.figure()
    plt.subplot(211)
    plt.plot(x)
    plt.subplot(212)
    plt.plot(xnorm)

    plt.show(block=True)



