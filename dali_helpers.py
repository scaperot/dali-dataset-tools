
import soundfile as sf

import os,time,sys,subprocess,librosa
import numpy as np

import DALI as dali_code
from DALI import utilities

def dali_setup():

    ################################
    # CHECK FOR DALI dataset folder
    ################################
    if os.path.isdir('DALI/'):
        dali_path = os.path.abspath('DALI/')
    else:
        print('DALI dataset not found in', os.path.abspath('.') + '/DALI/')
        sys.exit()

    ################################
    # CHECK FOR audio folder
    ################################
    if not os.path.isdir('audio/'):
        print('audio directory not found, trying to create it.')
        os.makedirs(os.path.abspath('.') + '/audio/')
    audio_path = os.path.abspath('audio/')

    dali_info = dali_code.get_info(dali_path + '/info/DALI_DATA_INFO.gz')
    return dali_path, audio_path, dali_info


#using Gupta's lyric preprocessing function...
#need to check licensing, etc.
# Changes: added # and @ to removed characters
#          returns lower case, not upper
# TODO: For now, copied from dali-lyric-analysis.py,
#       should put in a common file and import instead
def CleanUpLyrics(lyrics_raw):
    line = lyrics_raw.lower()
    regex = re.compile('[$*=:;/_,\.!?#@"\n]')  # Added # and @
    stripped_line = regex.sub('', line)
    if stripped_line == '': return
    check_for_bracket_words = stripped_line.split(' ')
    non_bracket_words = []

    for elem in check_for_bracket_words:
        if elem == "": continue #remove extra space
        if '(' in elem or ')' in elem: continue
        if elem[-1] == '\'': elem = elem.replace('\'','g') #Check if "'" is at the end of a word, then replace it with "g", eg. makin' => making
        if elem=="'cause": elem="cause"
        elem=elem.replace('-',' ')
        elem=elem.replace('&','and')
        non_bracket_words.append(elem)
    stripped_line = ' '.join(non_bracket_words)
    return stripped_line

def print_raw_transcript(song_id):
    '''
    prints every DALI paragraph to the screen

    Input: 
    song_id (string) - DALI song identification number

    Return:
    N/A
    '''
    dali_path, audio_path, dali_info = dali_setup()
    dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
    dali_entry = dali_data[song_id]

    artist   = dali_entry.info['artist']
    title    = dali_entry.info['title']
    language = dali_entry.info['metadata']['language']
    print(song_id,', title:',title,', artist:',artist,', language:',language)

    annot = dali_entry.annotations['annot']
    for i in range(len(annot['paragraphs'])):
        words = annot['paragraphs'][i]['text']
        time = annot['paragraphs'][i]['time']
        time_str = '%2.f, %.2f' % (time[0],time[1])
        print('Paragraph:',i,', ',time_str,', ',words)

def get_cropped_transcripts(dali_annot,song_ndx,sample_rate):
    '''
    Input:
    dali_annot (DALI object) - 
    song_ndx (mx2 numpy array) - values are samples relative to beginning of song (i.e. 0 is first sample) 
            row - [start of window, termination of window]
            m windows that were created with crop_song

    Return:
    song_transcripts (list)
    '''
    #find the words and times in an array for faster access...?  i'm not sure if its faster.
    mcrops = song_ndx.shape[0]
    song_transcripts = []
    for j in range(mcrops):
        start = song_ndx[j,0] / sample_rate
        term  = song_ndx[j,1] / sample_rate
        window_secs  = np.array([start,term])

        song_transcripts.append(get_transcript_for_window(dali_annot,window_secs))

        #print('window:',window_secs, ', crop num:',j,', transcript:',song_transcript[j])
    return song_transcripts

def is_song_trainable(dali_entry):
    '''
    filter out songs by metadata
    - only do english lyrics for now. (~75% of DALI dataset)
    - TODO: blacklist (i.e. load a list of songs to ignore) poorly transcribed songs
            (manual analysis)

    '''
    language = dali_entry.info['metadata']['language']
    if language != 'english':
        print('is_song_trainable: language: ',language,', id:',dali_entry.info['id'],', title:',dali_entry.info['title'],'artist:',dali_entry.info['artist'])
        return False
    
    #annotation type is generic to all labels (AFAIK)
    #
    #annot_type = dali_data.annotations['type']
    #if annot_type != 'horizontal':
    #    return False
    
    #number of lines should be ok as long as the songs are 
    # shuffled when performing training.  its possible 
    # they are signifcantly longer than other songs, there
    # would be some overfit to the distribution, but that
    # would have to be pretty large.
    #annot = dali_data.annotations['annot']['lines']
    #if len(annot) > 100:
    #    return False
    #
    # TODO: Possibly filter out more songs, like those that have long instrumental sections
    # print(dali_data.annotations.keys())
    # print(dali_data.annotations['annot_param'])
    # print(dali_data.annotations)
    # print(dali_data)
    # print([(i['time'], i['text']) for i in annot])
    # print([(i['time'], i['text']) for i in dali_code.annot2frames(annot, 1/22050)])
    return True

def calc_window_for_song(total_length,win_samples):
    '''
    calculate the start / end index for training windows
    slide window over song every (win_samples / 2) samples.

    Input:
    total_length (int) - total samples in a song
    win_samples (int) -  window size

    Return:
    start_ndx (m,) numpy array, the start of each window relative to the total samples of the song
    end_ndx (m,) numpy array, the end of each window relative to the total samples of song
    '''
    n   = np.arange(total_length)  # counter from 0 to max samples of x
    delta_samples = np.floor(win_samples / 2).astype(int)
    ndx = n[::delta_samples][:-1] # takes every win_samples of n, then remove the last sample
    start_ndx = np.reshape(ndx,(ndx.shape[0],1))
    end_ndx   = start_ndx+win_samples
    return np.concatenate((start_ndx, end_ndx),axis=1)

def crop_song(song_id, audio_path, dali_entry, win_samples):
    '''
    crop_song - takes a DALI song and crops it m times into win_length samples.

    Inputs: 
       song_id    - DALI song id
       entry      - DALI data entry
       audio_path - absolute path where audio files are stored (read/write)
       win_samples - number of samples for each crop
    Return:
       song_ndx   - (m,start_sample,stop_sample) indices for the m crops
       filename_list - absolute path for filenames saved with save_samples_wav

    1. load song with librosa
    2. calculate indices (i.e. sample index starting at 0) for windows of chunks. 
       a. 'win_rate' is win_length/2
       b. do not keep parts of the song less than win_length
    3. crop according to indices and save to audio_path in the form
        audio/<song_id>_##.wav 
        where ## is the number of chunks in the song.
    '''
    xin, sr = librosa.load(audio_path + '/' + song_id + '.wav', sr=None)
    x = normalize_data(xin)

    song_ndx = calc_window_for_song(x.shape[0],win_samples)

    l = song_ndx.shape[0]

    filename_list = []
    for i in range(l):
        filename_list.append( save_samples_wav(song_id, audio_path, i, x, (song_ndx[i,0],song_ndx[i,1]), sr) )

    return song_ndx, filename_list

def normalize_data(data):
    '''
    adjust the data from 1 to -1.
    '''
    xmin = np.min(data)
    xmax = np.max(data)
    return (2*(data - xmin) / (xmax-xmin+1e-10)-1)

def download_song(song_id, dali_info, audio_path, sample_rate):
    '''
    download_song: 
        1. download <song_id> from youtube.com
        2. save as audio/<song_id>.mp3
        3. convert to audio/<song_id>.wav (resample at sample_rate too)

    Input: 
    song_id   - (string) DALI song ID 
    dali_info - (DALI object) DALI song information needed to download song (URL, etc.)
    path      - (string) absolute path of destination for audio files
    sample_rate - (int) sampling rate used when converting to .wav

    Return:
    full path to song
    '''
    basename = audio_path + '/' + song_id

    # download...
    errors = dali_code.get_audio(dali_info, audio_path, skip=[], keep=[song_id])
    print(errors)
    i = 0

    # wait for download to finish...
    while utilities.check_file(basename + '.mp3') != True and i < 10:
        time.sleep(1)
        i += 1
        print('Waiting:',i,'seconds...')
    if i == 10:
        #try one more time...
        errors = dali_code.get_audio(dali_info, audio_path, skip=[], keep=[song_id])
        print(errors)

    # convert to .wav and resample to sample_rate
    print('Creating', basename + '.wav')
    subprocess.call(['ffmpeg', '-i', basename + '.mp3', '-ar', str(sample_rate), basename + '.wav'])

    # remove mp3...
    print('Removing', basename + '.mp3')
    os.remove(basename + '.mp3')
    return (basename+'.wav')

def generate_wav_file_name(song_id, audio_path, id_num):
    '''
    generating a filename for .wav files for training data

    Input:
    song_id       (string) DALI song ID, used as basename
    audio_path    (string) folder to save to
    id_num        (int) used to append to the name of the file.  can be something specific like line number
                         or just an arbitrary counter.

    Return:
    filename
    '''

    id_str = str(id_num).zfill(3)
    if id_num >= 1000:
        print('YIKES.  save_samples_wav - more than 1000 segments?')
        sys.exit()

    return audio_path + '/' + song_id + '_' + id_str + '.wav'

def save_samples_wav(song_id, audio_path, id_num, x, window_samples, sr):
    '''
    Inputs:
    song_id       (string) DALI song ID, used as basename
    audio_path    (string) folder to save to
    id_num        (int) used to append to the name of the file.  can be something specific like line number
                         or just an arbitrary counter.
    x             (numpy array) song samples of entire song
    window_samples  (tuple) (start,end) window of samples to save to disk


    Return:
    filename with no path      (string)
    absolute path and filename (string)
    '''
    n = x.shape[0]
    filename = generate_wav_file_name(song_id,audio_path,id_num)
    
    start = window_samples[0]
    term = window_samples[1]
    
    #print('Writing:', filename,',',window_samples)
    sf.write(filename, x[start:term], sr)
    return filename

def get_transcript_for_window(dali_annot,window_secs):
    '''
    Input:
    dali_annot (DALI object) - created using entry.annotations['annot']
    window_secs (tuple) - (start of window in secs,end of window in secs)
    
    Return:
    transcript (string)
    '''
    transcript = ''
    for i in range(len(dali_annot['words'])):
        #find first full onset word
        word = dali_annot['words'][i]['text']
        word_time  = dali_annot['words'][i]['time'] 
        # word starts after  the start of window 
        # word ends   before the end   of window 
        if word_time[0] > window_secs[0] and word_time[1] < window_secs[1]:
            transcript += (word + ' ')

    return transcript



if __name__ == '__main__':
    '''
    helpers is misc functions that are used over and over again for data wrangling
            below setup is checking to make sure DALI is in the local directory
            and that there is a folder to put audio files (if necessary) and make 
            one if necessary.
    '''
    dali_path, audio_path, dali_info = dali_setup()
    song_id = '3698c37beab64ec39196875d69720822'
    dali_entry = dali_code.get_the_DALI_dataset(dali_path, keep=[song_id])[song_id]
