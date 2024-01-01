import time
import keyboard
import serial
import pyvisa

# Number of times to run the increment system
samples = 86
center_freq = 3.1

filename = "C:/Users/mkouc/OneDrive/Notebooks/Automation/measurement_files" + time.strftime("%Y%m%d%H%M%S") + ".csv"
# Connect with spectrum analyzer
rm = pyvisa.ResourceManager()
my_instrument = rm.open_resource('USB0::0x0B5B::0xFFF9::1216060_1736_36::INSTR')

# Configure the serial connection to the motion controller
ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
# Set Speeds 
cmd = '2UV 20;' 
ser.write(cmd.encode('ascii'))
# Reading the data from the serial port
# Start arm at -90 degrees
cmd = '2UP -86; 2WS\r\n'
angle = -86
ser.write(cmd.encode('ascii'))
# Set center frequency and marker
my_instrument.write(':sens:freq:cent %fGHz' % center_freq)
my_instrument.write(':calc:mark:x %fGHz' % center_freq)
# Wait for arm to move to -90 degrees
time.sleep(7)
cmd = '2UV 8;' 
ser.write(cmd.encode('ascii'))
# Read marker value
f = open(filename, "w")
f.write("Angle, dBm\n")
value = my_instrument.query_ascii_values(':calc:mark:y?')
print("Arm at: ", angle)
print("\tdBm value: ", value)
f.write(str(angle) + "," + str(value).strip("[]") + "\n")
f.close()
# Increment the arm by 10 degrees
cmd = '2UR 2; 2WS\r\n'
i = 0

while i < samples:
    try:
        # Send command to increment arm by 2 degrees
        ser.write(cmd.encode('ascii'))
        angle += 2
        i += 1
        print("Arm at: ", angle)
        # Wait for arm to move 
        time.sleep(3)
        # Read marker value
        value = my_instrument.query_ascii_values(':calc:mark:y?')
        time.sleep(0.1)
        print("\tdBm value: ", value)
        f = open(filename, "a")
        f.write(str(angle) + "," + str(value).strip("[]") + "\n")
        f.close()
        value = 0
        # Buffer time
        time.sleep(1)
    except KeyboardInterrupt:
        print("Program stopped, arm at: ", angle)
        break
# Reset arm back to 0 degrees
cmd = '2UV 20;' 
ser.write(cmd.encode('ascii'))
cmd = '2UP 0; 2WS\r\n'
angle = 0
ser.write(cmd.encode('ascii'))
print("Arm at: ", angle)

