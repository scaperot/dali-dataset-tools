import numpy as np
import dali_helpers

if __name__ == '__main__':
    
    song_list = {}
    song_list['paren']       = dali_helpers.get_parenthetical_char_songs()
    song_list['replacement'] = dali_helpers.get_replacement_char_songs()

    #1. test for random song / random paragraph
    print('***** TEST 1: Random Song / Paragraph *****')
    n = np.random.randint(5358)
    paragraph_id = 2
    song_id    = dali_helpers.get_songid_by_index(n)
    transcript = dali_helpers.get_transcript(song_id,paragraph_id) 
    tclean     = dali_helpers.clean_up_lyrics(transcript,song_id,song_list)
    print('    Before:',transcript)
    print('    After:',tclean,end='\n\n')

    #2a. test for song with parens (with space)
    print('***** TEST 2a: Parens to Spaces: *****')
    song_id      = '050c5407c3cf421ea65c1d0dbc52137f'
    paragraph_id = 14
    transcript = dali_helpers.get_transcript(song_id,paragraph_id) 
    tclean     = dali_helpers.clean_up_lyrics(transcript,song_id,song_list)
    print('    Before:',transcript)
    print('    After:',tclean,end='\n\n')

    #2b. test for song with parens (with purge)
    print('***** TEST 2b: Purge Parens: *****')
    song_id = '024c9036742d4fcca03af2c8cee1553d'
    paragraph_id = 2
    transcript = dali_helpers.get_transcript(song_id,paragraph_id) 
    tclean     = dali_helpers.clean_up_lyrics(transcript,song_id,song_list)
    print('    Before:',transcript)
    print('    After:',tclean,end='\n\n')

    #3a. test for song with replacement (with literal)
    print('***** TEST 3a: Replacement characters with literal (% or $): *****')
    song_id = '98b07293bb5742e8825a065200d9e448'
    paragraph_id = 11
    transcript = dali_helpers.get_transcript(song_id,paragraph_id) 
    tclean     = dali_helpers.clean_up_lyrics(transcript,song_id,song_list)
    print('    Before:',transcript)
    print('    After:',tclean,end='\n\n')

    #3b. test for song with replacement (with spaces)
    print('***** TEST 3b: Replacement characters with literal (& or `): *****')
    song_id = 'b9696b1aad60461e94f020133ccdde84'
    paragraph_id = 5
    transcript = dali_helpers.get_transcript(song_id,paragraph_id) 
    tclean     = dali_helpers.clean_up_lyrics(transcript,song_id,song_list)
    print('    Before:',transcript)
    print('    After:',tclean,end='\n\n')

    #4. test for song with remove 
    print('***** TEST 4: Remove characters: *****')
    song_id = '4278bd68740640aaaa87a16b051f7b54'
    paragraph_id = 5
    transcript = dali_helpers.get_transcript(song_id,paragraph_id) 
    tclean     = dali_helpers.clean_up_lyrics(transcript,song_id,song_list)
    print('    Before:',transcript)
    print('    After:',tclean,end='\n\n')
