import numpy as np

import hvc.audio
import hvc.evfuncs

class test_audio():
    
    def test_spect():
        dat, fs = hvc.evfuncs.load_cbin('./test_data/cbins/'
                                        'gy6or6_baseline_240312_0811.1165.cbin')
        assert type(dat) == np.ndarray
        assert dat.dtype == '>i2' # should be big-endian 16 bit
        assert type(fs) == int