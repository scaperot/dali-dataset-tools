import numpy as np
import os, argparse
import DALI as dali_code
from DALI import utilities

import dali_helpers


'''
Take a single song and break up into ~10s chunks 
NOTE 1: This is a modification to Stoller's 'End to end lyrics alignment for polyphonic music 
  using an audio-to-character recogition model.', in which this code does not use context windows 
  on each side of the 10s prediction window.

Data Metadata Formata
- 225501 samples @22050Hz (10.2268s)

For Training: 
- shift 112750 samples @22050Hz (5.11s)

TODO: For Prediction
- shift by the size of the total samples (i.e. no overlap).

'''



def append_timing(audio_filename,timing_list):
    '''
    save wordonset.txt file of timing information for a file in jamendolyrics file format.

    Input:
    audio_filename (string) - filename of the audio file
    timing_list (list <float>) - word onset list

    1. basename - removes .wav from filename
    2. writes to basename.wordonset.txt (jamendolyric format)
    '''
    if audio_filename[-4:] != '.wav':
        print('append_timing: error, do not support other file types.')
        return False

    base_filename = audio_filename[:-4]
    txt_filename  = base_filename + '.wordonset.txt'
    
    f = open(txt_filename,'w')
    for i in timing_list:
        txt = '%.2f\n' % (i)
        f.write(txt)
    f.close()
    
    return

def append_transcript_nemo(json_filename,audio_filename,duration,transcript):
    '''
    append_transcript: save in nemo manifest format
       json_filename:  filename for appending
       audio_filename: absolute path to audio file
       duration:      length of song at full_filename
       transcript:    lyrics corresponding to full_filename
    '''
    jsonfile = open(json_filename, 'a')
    line_format = "{}\"audio_filepath\": \"{}\", \"duration\": {}, \"text\": \"{}\"{}"
    jsonfile.write(line_format.format(
            "{", audio_filename, duration, transcript, "}\n"))
    jsonfile.close()
    return


def preprocess_song(song_id, dali_path, audio_path, dali_info, nemo_manifest_filename, sample_rate):
    '''
    
    '''
    win_size = 10.2268
    win_samples = np.floor(win_size * sample_rate).astype(int)
    print('window samples: ',win_samples)

    dali_entry = dali_code.get_the_DALI_dataset(dali_path, keep=[song_id])[song_id]
    
    if dali_helpers.is_song_trainable(dali_entry):

        # get song and save to audio_path
        dali_helpers.download_song(song_id, dali_info, audio_path, sample_rate)

        # slice up song and save to audio_path, return indices of samples
        song_ndx,filename_list = dali_helpers.crop_song(song_id, audio_path, dali_entry, win_samples)


        # slice up the transcript for each cropped version of the song
        dali_annot = dali_entry.annotations['annot']
        transcript_list, timing_list = dali_helpers.get_cropped_transcripts(song_id, dali_annot,song_ndx,sample_rate)

        # save all cropped files in nemo format
        for i in range(len(transcript_list)):
            append_transcript_nemo(nemo_manifest_filename,filename_list[i],win_size,transcript_list[i])
            append_timing(filename_list[i],timing_list[i])

        return True

    return False


if __name__ == '__main__':
    '''
    choose a random song, crop audio files, and massage transcripts into nemo toolkit format
    '''


    parser = argparse.ArgumentParser(description='choose a song and preprocess for nemo toolkit.')
    parser.add_argument('-s','--song-id', required=False,type=str,default='',
            help='dali song id. default=choose a random song.  examples: 3698c37beab64ec39196875d69720822')
    args = parser.parse_args()

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()
    allsongfilenames = utilities.get_files_path(dali_path, '.gz')


    #number of samples assumes 22kHz (Stoller) - 10.23s
    sample_rate = 22050 
    if args.song_id == '':
        #choose a random song...
        n = len(allsongfilenames)
        i = np.random.randint(n)
        song_id = os.path.relpath(allsongfilenames[i], dali_path).split('.')[0]
    else:
        song_id = args.song_id

    dali_entry = dali_code.get_the_DALI_dataset(dali_path, keep=[song_id])[song_id]
    print('choosing index:',i,', title:',dali_entry.info['title'])
    
    #preprocess a song
    nemo_manifest_filename = 'dali_training.json'
    if not preprocess_song(song_id, dali_path, audio_path, dali_info, nemo_manifest_filename, sample_rate):
        print('ERROR PREPROCESSING.')


