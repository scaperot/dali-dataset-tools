
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
    
    song_id = args.song_id
    dali_helpers.print_raw_transcript(song_id)
