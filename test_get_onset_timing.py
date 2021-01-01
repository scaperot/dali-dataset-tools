
import os,time,sys,argparse

import dali_helpers




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s','--song-id', required=False,type=str,default='3698c37beab64ec39196875d69720822',
            help='dali song id. default: 3698c37beab64ec39196875d69720822')

    args = parser.parse_args()
    
    song_id = args.song_id

    onset_timing = dali_helpers.get_onset_timing(song_id)

    print(type(onset_timing), onset_timing)


