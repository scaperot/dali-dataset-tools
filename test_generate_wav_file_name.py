
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
    
    song_id = '3698c37beab64ec39196875d69720822'
    audio_path = '/fake_path/'

    for i in [0,3,12,143, 1001]:
        print( dali_helpers.generate_wav_file_name(song_id,audio_path,i) )



