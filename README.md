# dali-dataset-tools
Helper scripts for modifying DALI datasets.  For more information on DALI see this page: https://github.com/gabolsgabs/DALI</br></br> </br></br>

dali_helper.py - pool of most functions for doing various tasks.</br></br>
test_<func name>.py function testing</br></br></br></br>

Installation:
1. follow instructions on https://github.com/gabolsgabs/DALI for getting access to dataset
2. cd ~  
3. git clone https://github.com/scaperot/dali-dataset-tools
4. cd dali-dataset-tools
5. mv /path_to_dali/DALI/ .  
TODO: need to add requirements.txt file for dependencies.

Notes on Installation:</br>
* all audio files will be stored to dali-dataset-tools/audio/

Simple Example:</br>

    python test_print_raw_transcript.py


Output will look something like:</br>

    Paragraph: 0 ,  it's late at night and i'm feeling down ther're couplesstandingon thestreet sharing summer kisses and silly sounds so i step inside pour a glass of     wine with a full glass and an empty heart i search for something to occupy my mind
    Paragraph: 1 ,  but you are in my head swimming forever in my head tangled in my dreams swimming forever -
    Paragraph: 2 ,  so i listen to the radio - and all the songs we used to know - - so i listen to the radio
