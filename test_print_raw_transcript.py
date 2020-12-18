
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
    parser.add_argument('-i','--song-index', required=False,type=int,default=-1,
            help='index found by calling get_file_path.  used in many of the scripts to perform analysis.  use this flag if you find this is easier to sift through data interactively. default: -1 (ignores by default)')

    args = parser.parse_args()
    
    if args.song_index < 0:
        song_id = args.song_id
        dali_helpers.print_raw_transcript(song_id,'paragraphs')
    else:
        song_index = args.song_index
        dali_helpers.print_raw_transcript_by_index(song_index,'paragraphs')
