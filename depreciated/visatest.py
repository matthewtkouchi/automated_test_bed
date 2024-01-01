import pyvisa
import time


center_freq = 3.51
rm = pyvisa.ResourceManager()

my_instrument = rm.open_resource('USB0::0x0B5B::0xFFF9::1216060_1736_36::INSTR')

#Set start and stop frequencies
#my_instrument.write(':sens:freq:star 1GHz')
#my_instrument.write(':Sens:freq:stop 6GHz')

#Set center frequency
my_instrument.write(':sens:freq:cent %fGHz' % center_freq)
time.sleep(1)
#Set marker at center frequency
my_instrument.write(':calc:mark:x 3.51GHz')
time.sleep(0.1)

test = my_instrument.query_ascii_values(':calc:mark:y?\n')
print(test)

