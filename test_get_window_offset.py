
import numpy as np

import dali_helpers




if __name__ == "__main__":

    print('Print window offset for ground truth alignment label calculations.')
    sample_rate = 22050
    for i in range(30):
        print(dali_helpers.get_window_offset(i,sample_rate))





