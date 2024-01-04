from common import *
from setup import _get_csv_folder_path
from setup import setup_items

# Function to run the SA code
def run_sa(setup_items, my_instrument, ser, ff_mode, Total_Paths):
    # Initialize test settings
    set_sa_settings(my_instrument, ff_mode)
    
    # Set flag to continue testing
    continue1 = 1

    while continue1:
        # Create a measurements folder to store data
        file_path = os.path.join(_get_csv_folder_path(setup_items['data']['meas_foldername']), "sa_" + time.strftime("%Y%m%d%H%M%S") + ".csv")
        setup_items['data']['meas_folderpath'] = file_path

        # Initializee the Plot
        plt.ion()
        x, y = [], []
        figure, ax = plt.subplots(figsize=(10,8))
        line1, = ax.plot(x,y)
        ax.set_xlim([-90,90])
        ax.set_ylim([-90,-40])
        ax.set_xlabel('Receiver Angle (Deg)')
        ax.set_ylabel('Received Power (dBm)')
        figure.canvas.draw()
        figure.canvas.flush_events()
        plt.pause(2)

        # Set Speeds 
        cmd = '2UV 15;' 
        ser.write(cmd.encode('ascii'))
        # Reading the data from the serial port
        # Start arm at -90 degrees
        cmd = '2UP '+ str(setup_items[ff_mode]['Start_Angle']) + '; 2WS\r\n'
        ser.write(cmd.encode('ascii'))

        # Create a file to store data
        f = open(file_path, "w")
        f.write("Angle,Power(dBm)\n")
        current_angle = int(setup_items[ff_mode]['Start_Angle'])
        print("Arm at: ", current_angle)

        f.close()

        print(setup_items[ff_mode]['Center_Freq'])

        # Wait for arm to move to -90 degrees
        time.sleep(7)
        cmd = '2UV 8;' 
        ser.write(cmd.encode('ascii'))


        # Read all markers
        time.sleep(4)   # Wait for averaging to finish 
        value = my_instrument.query_ascii_values(':calc:mark:y?')
        print(f"Freq: {setup_items[ff_mode]['Center_Freq']}")
        print(f"Value: {value} dB")

        # Write to file
        f = open(file_path, "a")
        f.write(str(current_angle) + "," + str(value).strip("[]") + "\n")
        f.close()

        #re
        y.append(value)
        x.append(current_angle)

        line1.set_xdata(x)
        line1.set_ydata(y)

        figure.canvas.draw()

        figure.canvas.flush_events()

        # Increment the arm by 10 degrees
        cmd = '2UR '+ str(setup_items[ff_mode]['Step_Size']) + '; 2WS\r\n'

        while current_angle + int(setup_items[ff_mode]['Step_Size']) <= int(setup_items[ff_mode]['Stop_Angle']):
            try:
                # Send command to increment arm by 2 degrees
                ser.write(cmd.encode('ascii'))
                current_angle += int(setup_items[ff_mode]['Step_Size'])
                print("Arm at: ", current_angle)
                # Wait for arm to move + NA to finish averaging
                time.sleep(4)
                # Read all markers
                value = my_instrument.query_ascii_values(':calc:mark:y?')
                print(f"Freq: {setup_items[ff_mode]['Center_Freq']}")
                print(f"Value: {value} dB")
                time.sleep(0.1)
                f = open(file_path, "a")
                #Write to file
                f.write(str(current_angle) + "," + str(value).strip("[]") + "\n")
                f.close()

                y.append(value)
                x.append(current_angle)

                line1.set_xdata(x)
                line1.set_ydata(y)

                figure.canvas.draw()

                figure.canvas.flush_events()

                # Buffer time for the file to be written to
                time.sleep(3)
            except KeyboardInterrupt:
                print("Program stopped, arm at: ", current_angle)
                break
        # Reset arm back to 0 degrees
        cmd = '2UV 15;' 
        ser.write(cmd.encode('ascii'))
        cmd = '2UP 0; 2WS\r\n'
        angle = 0
        ser.write(cmd.encode('ascii'))
        print("Arm at: ", angle)

        Total_Paths.append(file_path)

        data = pd.read_csv(file_path)
        holder_data = np.array(data['Power(dBm)'].values)
        data['Normalized Power (dB)'] = holder_data-max(holder_data)
        data.to_csv(file_path, index=False)

        time.sleep(4)

        root = tk.Tk()
        root.withdraw()
        continue1 = tk.messagebox.askyesno(
            message="Do you want to perform another test?",
            title="Radiation Pattern Automation Code"
        )
        plt.close()

# Function to run the NA code (TO BE ADDED)
def run_na(setup_items, my_instrument, ser, ff_mode, Total_Paths):
    # Initialize test settings
    set_na_settings(my_instrument, ff_mode)

    # Set flag to continue testing
    continue1 = 1

    while continue1:
        # Create a measurements folder to store data
        file_path = os.path.join(_get_csv_folder_path(setup_items['data']['meas_foldername']), "na_" + time.strftime("%Y%m%d%H%M%S") + ".csv")
        setup_items['data']['meas_folderpath'] = file_path

        # Initializee the Plot
        plt.ion()
        x, y = [], []
        figure, ax = plt.subplots(figsize=(10,8))
        line1, = ax.plot(x,y)
        ax.set_xlim([-90,90])
        ax.set_ylim([-90,-40])
        ax.set_xlabel('Receiver Angle (Deg)')
        ax.set_ylabel('Received Power (dBm)')
        figure.canvas.draw()
        figure.canvas.flush_events()
        plt.pause(2)

        # Set Speeds 
        cmd = '2UV 15;' 
        ser.write(cmd.encode('ascii'))
        # Reading the data from the serial port
        # Start arm at -90 degrees
        cmd = '2UP '+ str(setup_items[ff_mode]['Start_Angle']) + '; 2WS\r\n'
        ser.write(cmd.encode('ascii'))

        # Create a file to store data
        f = open(file_path, "w")
        f.write("Angle,Power(dBm)\n")
        current_angle = int(setup_items[ff_mode]['Start_Angle'])
        print("Arm at: ", current_angle)

        f.close()

        print(setup_items[ff_mode]['Center_Freq'])

        # Wait for arm to move to -90 degrees
        time.sleep(7)
        cmd = '2UV 8;' 
        ser.write(cmd.encode('ascii'))


        # Read all markers
        time.sleep(6)   # Wait for averaging to finish
        
        # Enable time gating if the user wants it
        if (setup_items[ff_mode]['Enable_Gating']):
            enable_time_gate(my_instrument, ff_mode)  # Note that time gating is still enabled after returning here but transform is off
            
        value = my_instrument.query_ascii_values(':calc:mark:y?')
        print(f"Freq: {setup_items[ff_mode]['Center_Freq']}")
        print(f"Value: {value} dB")

        # Write to file
        f = open(file_path, "a")
        f.write(str(current_angle) + "," + str(value).strip("[]") + "\n")
        f.close()

        #re
        y.append(value)
        x.append(current_angle)

        line1.set_xdata(x)
        line1.set_ydata(y)

        figure.canvas.draw()

        figure.canvas.flush_events()

        # Increment the arm by step size
        cmd = '2UR '+ str(setup_items[ff_mode]['Step_Size']) + '; 2WS\r\n'

        while current_angle + int(setup_items[ff_mode]['Step_Size']) <= int(setup_items[ff_mode]['Stop_Angle']):
            try:
                # Send command to increment arm by step size
                ser.write(cmd.encode('ascii'))
                current_angle += int(setup_items[ff_mode]['Step_Size'])
                print("Arm at: ", current_angle)
                # Wait for arm to move + NA to finish averaging
                time.sleep(6)
                # Read all markers
                # Enable time gating if the user wants it
                if (setup_items[ff_mode]['Enable_Gating']):
                    enable_time_gate(my_instrument, ff_mode)  # Note that time gating is still enabled after returning here but transform is off
                value = my_instrument.query_ascii_values(':calc:mark:y?')
                print(f"Freq: {setup_items[ff_mode]['Center_Freq']}")
                print(f"Value: {value} dB")
                time.sleep(0.1)
                f = open(file_path, "a")
                #Write to file
                f.write(str(current_angle) + "," + str(value).strip("[]") + "\n")
                f.close()

                y.append(value)
                x.append(current_angle)

                line1.set_xdata(x)
                line1.set_ydata(y)

                figure.canvas.draw()

                figure.canvas.flush_events()

                # Buffer time for the file to be written to
                time.sleep(3)
            except KeyboardInterrupt:
                print("Program stopped, arm at: ", current_angle)
                break
        # Reset arm back to 0 degrees
        cmd = '2UV 15;' 
        ser.write(cmd.encode('ascii'))
        cmd = '2UP 0; 2WS\r\n'
        angle = 0
        ser.write(cmd.encode('ascii'))
        print("Arm at: ", angle)

        Total_Paths.append(file_path)

        data = pd.read_csv(file_path)
        holder_data = np.array(data['Power(dBm)'].values)
        data['Normalized Power (dB)'] = holder_data-max(holder_data)
        data.to_csv(file_path, index=False)

        time.sleep(4)

        root = tk.Tk()
        root.withdraw()
        continue1 = tk.messagebox.askyesno(
            message="Do you want to perform another test?",
            title="Radiation Pattern Automation Code"
        )
        plt.close()


# Function to read all csv files from the Total_Paths to an array
def read_csv_files(Total_Paths, Unnormalized_Data, Normalized_Data):
    first = 1
    k = 1
    for path in Total_Paths:
        df = pd.read_csv(path)
        if first:
            holder3 = np.array(df['Angle'].values)
            Unnormalized_Data = pd.DataFrame(holder3, columns =['Angle'])
            Normalized_Data = pd.DataFrame(holder3, columns =['Angle'])
        holder1 = np.array(df['Power(dBm)'].values)
        Unnormalized_Data = Unnormalized_Data.assign(**{f'Test_{k}' : holder1})
        holder2 = np.array(df['Normalized Power (dB)'].values)
        Normalized_Data = Normalized_Data.assign(**{f'Test_{k}' : holder2})
        first = 0
        k += 1

def get_axis_data(Unnormalized_Data, Normalized_Data):
    # X-axis data is the same for both plots (frequency)
    x_data = Unnormalized_Data["Angle"]
    
    # Initialize empty dictionaries to store y-axis data for unnorm and norm plots
    column_data, column_data_1 = {}, {}
    for column in Unnormalized_Data.columns:
        if column != "Angle":  # Skip the x-axis column
            column_data[column] = {"data": Unnormalized_Data[column], "display": False}
    for column in Normalized_Data.columns:
        if column != "Angle":  # Skip the x-axis column
            column_data_1[column] = {"data": Normalized_Data[column], "display": False}
            
    return x_data, column_data, column_data_1
    
# Function to plot the data
def plot_data(ax, canvas, x_data, y_data_unnorm, y_data_norm):
    # Clear the existing plot in case this is a rerender of the plot 
    ax.clear()
    if setup_items['data']['Normalized']:
        for column, data_info in y_data_norm.items():
            if data_info["display"]:
                ax.plot(x_data, data_info["data"], label=column)
    else:
        for column, data_info in y_data_unnorm.items():
            if data_info["display"]:
                ax.plot(x_data, data_info["data"], label=column)
                
    ax.set_xlabel("Angle [deg]")
    ax.set_ylabel("Power [dBm]")
    ax.set_title("Overlay of Multiple Plots")
    ax.legend()
    ax.grid(True)
    canvas.draw()

# Function to toggle the "display" property of the columns
def toggle_display(column, y_data_unnorm, y_data_norm, ax, canvas, x_data):
    y_data_unnorm[column]["display"] = not y_data_unnorm[column]["display"]
    y_data_norm[column]["display"] = not y_data_norm[column]["display"]
    plot_data(ax, canvas, x_data, y_data_unnorm, y_data_norm)
    
# Click handler for normalizing the collected data plots
def onNormalizedClick(Normalized, y_data_unnorm, y_data_norm, ax, canvas, x_data):
    if Normalized.get():
        setup_items['data']['Normalized'] = 1
        plot_data(ax, canvas, x_data, y_data_unnorm, y_data_norm)
    else:
        setup_items['data']['Normalized'] = 0
        plot_data(ax, canvas, x_data, y_data_unnorm, y_data_norm)
        
def set_sa_settings(my_instrument, ff_mode):
    # Number of times to run the increment system
    center_freq = float(setup_items[ff_mode]['Center_Freq'])   # Hz
    freq_span = float(setup_items[ff_mode]['Span'])     # Hz
    videobw = float(setup_items[ff_mode]['VBW'])     # Hz
    resbw = float(setup_items[ff_mode]['RBW'])       # Hz
    average_passes = 1

    # Set center freq then frequency span markers
    my_instrument.write(':sens:freq:cent %f' % center_freq)
    my_instrument.write(':sens:freq:span %f' % freq_span)
    my_instrument.write(':sens:aver:coun %f' % average_passes)
    my_instrument.write(':sens:band:res %f' % resbw)
    my_instrument.write(':sens:band:vid %f' % videobw)
    # Activate marker 1 and set it to the center frequency
    my_instrument.write('CALC:MARK1:ACT')
    my_instrument.write('CALC:MARK:X %f' % center_freq)
        
def set_na_settings(my_instrument, ff_mode):
    # Number of times to run the increment system
    center_freq = float(setup_items[ff_mode]['Center_Freq'])   # Hz
    freq_span = float(setup_items[ff_mode]['Span'])     # Hz
    ifbw = float(setup_items[ff_mode]['IFBW'])     # Hz

    # Set power settings
    my_instrument.write(':sour:pow' % setup_items[ff_mode]['Power'])
    # Set frequency settings
    my_instrument.write(':sens:freq:cent %f' % center_freq)
    my_instrument.write(':sens:freq:span %f' % freq_span)
    my_instrument.write(':sens:swe:poin %d' % setup_items[ff_mode]['Num_Points'])
    # Set sweep settings
    my_instrument.write(':sens:aver:coun %f' % setup_items[ff_mode]['Average_Passes'])
    my_instrument.write(':sens:aver:mode %s' % setup_items[ff_mode]['Average_Mode'])
    my_instrument.write('sense:bwid %f' % ifbw)
    # Set Scale Settings
    my_instrument.write(':DISP:TRAC1:Y:PDIV %f' % setup_items[ff_mode]['Scale'])
    my_instrument.write(':DISP:TRAC1:Y:RLEV %f' % setup_items[ff_mode]['Ref_Lvl'])
    # Set Trigger Settings
    my_instrument.write(':TRIG:SOUR %d' % setup_items[ff_mode]['Trigger_Source'])
    # Create a S21 measurement 
    my_instrument.write('CALC:PAR1:DEF S21')
    my_instrument.write('CALC:PAR1:SEL')
    # Create peak search marker for time gating and center freq marker (active)
    my_instrument.write('CALC:MARK1: ON')
    my_instrument.write('CALC:MARK2: ON')
    my_instrument.write('CALC:MARK1:ACT')
    my_instrument.write('CALC:MARK:X %f' % center_freq)  
    # Set time domain settings
    my_instrument.write(':calc:tran:time:star %f' % setup_items[ff_mode]['Start_Time'])
    my_instrument.write(':calc:tran:time:stop %f' % setup_items[ff_mode]['Stop_Time'])
    
    
# Enable time gating on the current NA trace
# The final trace should return to the frequency domain, but with gating enabled
def enable_time_gate(my_instrument, ff_mode):
    # Transform ON
    my_instrument.write(':calc:tran:time:stat 1')
    # Trigger a single sweep
    my_instrument.write(':init:imm')
    # Wait for acquisition to finish (might need increase based on average passes)
    time.sleep(10)  
    # Activate marker 2 and set it to the max value (dB)
    my_instrument.write(':calc:mark2:act')
    my_instrument.write(':calc:mark2:func:max')
    # Get x-axis value of marker 2
    peak_time = float(my_instrument.write(':calc:mark2:x?'))
    # Set time gating markers around the peak value
    my_instrument.write(':calc:filt:time:cent %f' % peak_time)
    my_instrument.write(':calc:filt:time:span %f' % setup_items[ff_mode]['Time_Gate_Width'])
    # Turn gating on
    my_instrument.write(':calc:filt:time:stat 1')
    # Turn transform off
    my_instrument.write(':calc:tran:time:stat 0')
    # Return active marker to center frequency
    my_instrument.write(':calc:mark1:act')
    
    return
    