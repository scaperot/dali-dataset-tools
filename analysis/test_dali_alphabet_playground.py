import numpy as np

special_alphabet=['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`','{', '}']

def char_exists(input_str):
    '''
    check to see if there is a special character in the string.
    1. char.find - looks at string and reports the highest index 
                   in input_str.  returns the size of special_alphabet.
                   returns -1 for an index if the there is not a numeric
                   character of that type.
    2. max - look for anything that is above -1 which indicates that a 
             char is present.

    Input:
    input_str (string) - string under evaluation.

    Return:
    True/False
    '''
    return (np.max(np.char.find(input_str,special_alphabet)) >= 0)

if __name__ == '__main__':
    data = np.load('dali_alphabet_histogram.npy',allow_pickle=True)
    d = data.item()
    vals = list(d.values())
    keys = list(d.keys())

    #create a list with key/valus that can be sorted in various ways
    data_list = []
    special_list = []
    for i in range(len(vals)):
        tup = (keys[i],vals[i])
        data_list.append(tup)
        if char_exists(keys[i]):
            special_list.append(tup)

    data_list.sort(key=lambda tup: tup[1])
    special_list.sort(key=lambda tup: tup[1],reverse=True)

    



