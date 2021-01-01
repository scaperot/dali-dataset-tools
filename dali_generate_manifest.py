import numpy as np
import os,time,sys,parseargs

import DALI as dali_code
from DALI import utilities

import dali_helpers


'''
given a dataset size smaller than all of DALI, generate a nemo manifest file
1. check if the song is in English or has prohibited features (is_song_trainable)
2. write manifest to disk
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-n','--number-of-songs', required=True,type=int,default=10,
            help='number of songs to find')
    
    sr = 22050

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()

    allsongfilenames = utilities.get_files_path(dali_path,'.gz')

    total_songs = len(allsongfilenames)
    number_of_songs = args.number_of_songs
    ndx = np.arange(total_songs)
    np.random.shuffle(ndx)
    
    songids = []
    i = 0
    while (len(songids) < number_of_songs):
        #import song metadata
        song_id =  os.path.relpath(allsongfilenames[i],dali_path).split('.')[0]
        dali_entry = dali_data[song_id]
        
        #if its a good song, then go for it!
        if dali_helpers.song_is_trainable(dali_entry):
            songids.append(song_id)
            transcript = dali_helpers.get_full_transcript(song_id)
            nemo_helpers.append_transcript_nemo(args.new_filename,audio_filename,0,transcript)

        i += 1
    print()

