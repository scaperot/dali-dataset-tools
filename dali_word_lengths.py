import matplotlib.pyplot as plt
import numpy as np
import os,time,sys

import pdb
import DALI as dali_code
from DALI import utilities

import dali_helpers

import logging


OUTLIER_WORD_LENGTH = 5  # in seconds


def word_length_histogram(data, ax):
    ax.hist(data, color='black',
            range=(0, OUTLIER_WORD_LENGTH),
            bins=100, density=True)
    # title = 'Word Lengths'
    title = duration_stats(data, 'DALI Word Lengths\n\n')
    ax.set_title(title)
    ax.set_xlabel('Word Length (s)')


def character_length_histogram(data, ax):
    means = data[:, 1] / data[:, 0]
    freq = data[:, 0]
    ax.hist(means, weights=freq,
            color='black', range=(0, 1),
            bins=100, density=True)
    # title = 'Character Lengths'
    title = character_duration_stats(data, 'DALI Character Lengths\n\n')
    ax.set_title(title)
    # text = character_duration_stats(data, "")
    # props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # ax.text(0.95, 0.95, text, transform=ax.transAxes, fontsize=12,
    #         verticalalignment='top', bbox=props)
    ax.set_xlabel('Character Length (s)')


def silence_histogram(data, ax):
    ax.hist(data, color='black',
            range=(0, OUTLIER_WORD_LENGTH),
            bins=100, density=True)
    # title = 'Within Song Non-vocal Segments'
    title = duration_stats(data, 'DALI Within Song Non-vocal Segments\n\n')
    ax.set_title(title)
    ax.set_xlabel('Non-vocal Length (s)')


def beginning_silence_histogram(data, ax):
    ax.hist(data, color='black',
            range=(0, 30),
            bins=100, density=True)
    # title = 'Beginning Non-vocal Segments'
    title = begin_silence_stats(data, 'DALI Beginning Non-vocal Segments\n\n')
    ax.set_title(title)
    ax.set_xlabel('Non-vocal Length (s)')


def duration_stats(delta, desc):
    format_string = desc + 'Mean = %.2f Std=%.2f min=%.2f max=%.2f\n'
    format_string += 'Below 1s: %.1f %% Below 5s: %.1f %%'
    stats_str = format_string % (np.mean(delta),
                                 np.std(delta),
                                 np.amin(delta),
                                 np.amax(delta),
                                 100 * np.count_nonzero(delta < 1) / delta.shape[0],
                                 100 * np.count_nonzero(delta < 5) / delta.shape[0])
    return stats_str


def begin_silence_stats(delta, desc):
    format_string = desc + 'Mean = %.2f Std=%.2f min=%.2f max=%.2f\n'
    format_string += 'Above 10s: %.1f %% Above 20s: %.1f %%'
    stats_str = format_string % (np.mean(delta),
                                 np.std(delta),
                                 np.amin(delta),
                                 np.amax(delta),
                                 100 * np.count_nonzero(delta > 10) / delta.shape[0],
                                 100 * np.count_nonzero(delta > 20) / delta.shape[0])
    return stats_str


def character_duration_stats(delta, desc):
    means = delta[:, 1] / delta[:, 0]
    freq = delta[:, 0]
    count = np.sum(freq)
    mean = np.sum(delta[:, 1]) / count
    var = np.sum((means - mean) * (means - mean) * freq) / count
    std = np.sqrt(var)

    format_string = desc + 'Mean = %.2f Std=%.2f min=%.2f max=%.2f\n'
    format_string += 'Below 100ms: %.1f %% Below 500ms: %.1f %%'
    stats_str = format_string % (mean,
                                 std,
                                 np.amin(means),
                                 np.amax(means),
                                 100 * np.sum(np.where(means < 0.1, freq, 0)) / count,
                                 100 * np.sum(np.where(means < 0.5, freq, 0)) / count)
    return stats_str


def analyse_word_lengths(delta, character_delta,
                         silence_delta, begin_silence_delta,
                         neg_length_count, zero_length_count,
                         neg_word_start_count, neg_word_end_count,
                         neg_silence_count, n_songs_no_words):
    print('Number of words:', delta.shape[0])
    print('Number of words reported negative length time:', neg_length_count)
    print('Number of words reported zero length time:', zero_length_count)
    print('Number of words with negative start time:', neg_word_start_count)
    print('Number of words with negative end time:', neg_word_end_count)
    print('Number of negative length silences: ', neg_silence_count)
    print('Number of songs with no words:', n_songs_no_words)

    print(duration_stats(delta, 'Word'))
    print(duration_stats(silence_delta, 'Within song silence'))
    print(begin_silence_stats(begin_silence_delta, 'Beginning silence'))
    print(character_duration_stats(character_delta, 'Mean character lengths'))

    fig, axs = plt.subplots(2, 2)
    word_length_histogram(delta, axs[0, 0])
    character_length_histogram(character_delta, axs[0, 1])
    silence_histogram(silence_delta, axs[1, 0])
    beginning_silence_histogram(begin_silence_delta, axs[1, 1])
    fig.tight_layout()
    plt.show(black=True)
    # fig.savefig('./analysis/dali_word_lengths_histogram.png')


def main():
    save_path = './analysis/dali_word_lengths_histogram.npy'
    character_path = './analysis/dali_character_lengths_histogram.npy'
    silence_path = './analysis/dali_silence_lengths_histogram.npy'
    begin_silence_path = './analysis/dali_begin_silence_lengths_histogram.npy'

    if (os.path.exists(save_path) and os.path.exists(character_path)
            and os.path.exists(silence_path)
            and os.path.exists(begin_silence_path)):
        delta = np.load(save_path)
        character_delta = np.load(character_path)
        silence_delta = np.load(silence_path)
        begin_silence_delta = np.load(begin_silence_path)
        analyse_word_lengths(delta, character_delta,
                             silence_delta, begin_silence_delta,
                             -1, -1, -1, -1, -1, -1)
        return

    logging.basicConfig(format='%(levelname)s:%(message)s',
                        filename='./analysis/word_lengths.log',
                        filemode='w',
                        level=logging.INFO)

    dali_path, audio_path, dali_info = dali_helpers.dali_setup()

    ################################################
    # Loading dali dataset
    # Loaded dali dataset in 69.43356609344482 seconds
    # Measure the length of words for 5358 songs...
    # [-----------------------------------------]
    # time to process 5358 songs: 6.159158945083618
    # Number of non-empty words with positive duration: 1373750
    # Number of words reported negative length time: 29
    # Number of words reported zero length time: 5
    # Number of words with negative start time: 433
    # Number of negative length silences:  2096
    # Number of songs with no words: 0
    # ###############################################
    # allsongfilenames = utilities.get_files_path(dali_path,'.gz')
    delta = []
    begin_silence_delta = []
    silence_delta = []
    character_delta = []
    # song_id = ''
    print("Loading dali dataset")
    start = time.time()
    dali_data = dali_code.get_the_DALI_dataset(dali_path)
    done = time.time()
    print("Loaded dali dataset in", (done - start), "seconds")
    n = len(dali_data)
    print("Measure the length of words for", n, "songs...")

    # setup toolbar
    toolbar_width = 40
    modulo_val = np.floor(n/toolbar_width).astype(int)
    sys.stdout.write("[%s]" % (" " * (toolbar_width+1)))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+2))  # return to start of line, after '['

    start = time.time()
    neg_length_count = 0
    zero_length_count = 0
    n_songs_no_words = 0
    neg_silence_count = 0
    neg_word_start_count = 0
    neg_word_end_count = 0
    for i, (song_id, entry) in enumerate(dali_data.items()):
        # import song metadata
        # song_id = os.path.relpath(allsongfilenames[i],dali_path).split('.')[0]
        # dali_data = dali_code.get_the_DALI_dataset(dali_path,keep=[song_id])
        # entry = dali_data[song_id]

        # get all words of song
        annot = entry.annotations['annot']['words']
        # word_times = [i['time'] for i in dali_code.annot2frames(annot, 1/sr)]
        word_times = [i['time'] for i in annot]
        words = [i['text'] for i in annot]
        nwords = len(word_times)
        if nwords == 0:
            n_songs_no_words += 1
            continue

        # Non-informative: End of the last word always matches end of the last note
        # Taken from DALI Github page: https://github.com/gabolsgabs/DALI
        # Comes with the following not very clear comment:
        # "the value dur is just an example you should use the end of your audio file"
        # end_of_the_song = entry.annotations['annot']['notes'][-1]['time'][1]
        # end_silence_delta.append(end_of_the_song - word_times[-1][1])

        silence_start_time = 0
        n_nonempty_words = 0
        for j in range(nwords):
            duration_secs = word_times[j][1] - word_times[j][0]
            # skip words with negative start time.
            if word_times[j][0] < 0:
                logging.info('NEGATIVE WORD START TIME: DALI ID: %s, index '
                             '(from get_file_path): %d, text: %s, '
                             'word length: %.2f, line number: %d',
                             song_id, i, annot[j]['text'], duration_secs, j)
                neg_word_start_count += 1
                silence_start_time = None
                continue

            # skip words with negative start time.
            if word_times[j][1] < 0:
                logging.info('NEGATIVE WORD END TIME: DALI ID: %s, index '
                             '(from get_file_path): %d, text: %s, '
                             'word length: %.2f, line number: %d',
                             song_id, i, annot[j]['text'], duration_secs, j)
                neg_word_end_count += 1
                silence_start_time = None
                continue

            # skip words with negative duration
            if duration_secs < 0:
                logging.info('NEGATIVE WORD LENGTH: DALI ID: %s, index '
                             '(from get_file_path): %d, text: %s, '
                             'word length: %.2f, line number: %d',
                             song_id, i, annot[j]['text'], duration_secs, j)
                neg_length_count += 1
                silence_start_time = None
                continue

            # skip empty words
            if not words[j]:
                if silence_start_time is None:
                    silence_start_time = words[j][0]
                continue

            n_nonempty_words += 1

            if silence_start_time is not None:
                silence_secs = word_times[j][0] - silence_start_time
                if silence_secs >= 0:
                    if silence_start_time == 0:
                        begin_silence_delta.append(silence_secs)
                    else:
                        silence_delta.append(silence_secs)
                else:
                    neg_silence_count += 1
            silence_start_time = word_times[j][1]

            if duration_secs > 0:
                delta.append(duration_secs)
                character_delta.append((len(words[j]), duration_secs))
            elif duration_secs == 0:
                zero_length_count += 1

            if duration_secs >= OUTLIER_WORD_LENGTH:
                # find outlier words
                logging.info('LONG WORD LENGTH: DALI ID: %s, '
                             'index (from get_file_path): %d, '
                             'text: %s, word length: %.2f, '
                             'word index: %d',
                             song_id, i, annot[j]['text'], duration_secs, j)

        if n_nonempty_words == 0:
            n_songs_no_words += 1

        if not (i % modulo_val):
            print('-', end='', flush=True)
    print('')

    done = time.time()
    delta = np.array(delta)
    character_delta = np.array(character_delta)
    silence_delta = np.array(silence_delta)
    begin_silence_delta = np.array(begin_silence_delta)
    print('time to process', n, 'songs:', done-start)
    np.save(save_path, delta)
    np.save(character_path, character_delta)
    np.save(silence_path, silence_delta)
    np.save(begin_silence_path, begin_silence_delta)

    analyse_word_lengths(delta, character_delta,
                         silence_delta, begin_silence_delta,
                         neg_length_count, zero_length_count,
                         neg_word_start_count, neg_word_end_count,
                         neg_silence_count, n_songs_no_words)


if __name__ == '__main__':
    main()
