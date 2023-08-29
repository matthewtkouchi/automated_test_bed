import time
import keyboard
import serial
import pyvisa

# Number of times to run the increment system
samples = 86
center_freq = 3.5  #GHz
freq_span = 600  #MHz
cur_freq = center_freq - 0.2
freq = []
values = []
angle = 86
average_passes = 2

filename = "C:/Users/mkouc/OneDrive/Notebooks/Automation/measurement_files" + time.strftime("%Y%m%d%H%M%S") + ".csv"

# Get the span of frequency points for the marker
for i in range(6):
    freq.append(cur_freq)
    cur_freq += 0.1
    cur_freq = round(cur_freq, 1)

# Connect with spectrum analyzer
rm = pyvisa.ResourceManager()
my_instrument = rm.open_resource('USB0::0x2A8D::0x5C18::SG62157030::INSTR')

# Create a file to store data
f = open(filename, "w")
f.write("Angle, dBm1, dBm2, dBm3, dBm4, dBm5, dBm6\n")

# Set NA Settings
my_instrument.write(':sens:freq:cent %fe9' % center_freq)
my_instrument.write(':sens:freq:span %fe6' % freq_span)
my_instrument.write(':sens:bwid 100')
my_instrument.write(':sens:aver:coun %f' % average_passes)

for i in range(1,7):
    my_instrument.write(':calc:mark%s:act' % i)
    my_instrument.write(':calc:mark%s:x %fe9' % (i, freq[i-1]))


# Test reading multiple markers
for i in range(1,7):
    values.append(my_instrument.query_ascii_values(':calc:mark%s:y?' %i))
    print(f"Freq: {freq[i-1]}")
    print(f"Value: {values[i-1][0]} dB")
    
f.write(str(angle) + "," + str(values[0][0]).strip("[]") + "," + str(values[1][0]).strip("[]") 
        + "," + str(values[2][0]).strip("[]") + "," + str(values[3][0]).strip("[]") 
         + "," + str(values[4][0]).strip("[]") + "," + str(values[5][0]).strip("[]") + "\n")

f.close()


