import os
import tkinter as tk
from enum import Enum
from tkinter import messagebox, ttk
import serial.tools.list_ports

# NA Trace Measurement Types
class MType(Enum):
    LOGMAG = 1
    LINEAR = 2
    VSWR = 3
    PHASE = 4
    SMITH = 5
    POLAR = 6
    REAL = 7
    IMAG = 8
    
# Declare dictionary to store widget mappings to tk entries
widget_mapping = {}

# All settings related to the motion controller frame
motion_frame_settings = ['COM_PORT', 'Start_Angle', 'Stop_Angle', 'Step_Size']

# Declare dictionaries to store setup items for SA, NA, and Motion Controller
setup_items = {
    'sa': {
        'INSTR_ID': None,
        'COM_PORT': None,
        'Start_Angle': -86,
        'Stop_Angle': 86,
        'Step_Size': 2,
        'Span': 600e6,
        'Center_Freq': 28e9,
        'VBW': 3e3,
        'RBW': 30e3,
    },
    'na': {
        'INSTR_ID': None,
        'COM_PORT': None,
        'Start_Angle': -2,
        'Stop_Angle': 2,
        'Step_Size': 2,
        'Span': 600e6, #Hz
        'Center_Freq': 3.5e9, #Hz
        'Num_Points': 201,
        'Average_Passes': 2,
        'Average_Mode': 'SWEEP', #SWEEP or POINT
        'IFBW': 10e3, # Hz
        'Scale': 5, #dB/division
        'Ref_Lvl': -20, #dB
        'Power': -10, #dBm : Set power level from +3 to -45 dBm in .1 dB steps
        'Trigger_Source': 'INT', #INT or EXT
        'Start_Time': -10e-9, #s
        'Stop_Time': 10e-9, #s
        'Time_Gate_Width': 20e-9, #s
        'Enable_Gating': 0, # 0 or 1
    },
    'data': {   # Most is not used as of now
        'meas_foldername': "measurement-files",
        'meas_folderpath': None,
        'Normalized': 0,
        'Trace_Format': MType.LOGMAG,
    }
}
        
        
def _get_csv_folder_path(folder_name):
    # Create csv folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    # Get the relative path to the folder
    rel_path = os.path.join(os.getcwd(), folder_name)
    return rel_path


def _get_ff_mode():
    # Create a GUI to select the FieldFox mode
    root = tk.Tk()
    root.title("Select FieldFox Mode")
    root.geometry("640x400")  
    root.resizable(False, False)  

    # Variable to store the selected mode
    selected_mode = tk.StringVar()
    
    def SA_press():
        selected_mode.set('sa')  
        root.destroy()

    def NA_press():
        selected_mode.set('na')  
        root.destroy()

    # Create buttons to select the mode
    tk.Label(root, text="Select FieldFox Mode:").grid(row=0)
    SA_button = tk.Button(root, text="Spectrum Analyzer", command=SA_press, height=1, width=20)
    SA_button.grid(row=1, column=0, columnspan=2, rowspan=2)
    NA_button = tk.Button(root, text="Network Analyzer", command=NA_press, height=1, width=20)
    NA_button.grid(row=3, column=0, columnspan=2, rowspan=2)
    root.mainloop()

    # Return the selected mode
    return selected_mode.get()

# Function to create labels for each setting entry
def create_tk_labels(frame, key, row):
    key_up = key.upper()
    if "FREQ" in key_up or "BW" in key_up or "SPAN" in key_up:
        tk.Label(frame, text=f"{key} (Hz):").grid(row=row)
    elif "ANGLE" in key_up or "STEP_SIZE" in key_up:
        tk.Label(frame, text=f"{key} (deg):").grid(row=row)
    elif "SCALE" in key_up or "REF" in key_up:
        tk.Label(frame, text=f"{key} (dB):").grid(row=row)
    elif "POWER" in key_up:
        tk.Label(frame, text=f"{key} (dBm):").grid(row=row)
    elif "TIME" in key_up:
        tk.Label(frame, text=f"{key} (s):").grid(row=row)
    elif "TRIGGER" in key_up:
        tk.Label(frame, text=f"{key} (INT or EXT):").grid(row=row)
    elif "ENABLE" in key_up:
        tk.Label(frame, text=f"{key} (0=OFF or 1=ON):").grid(row=row)
    else:
        tk.Label(frame, text=f"{key}:").grid(row=row)


# Function to create entry widget
def create_tk_entry(frame, row, col, setting, ff_mode):
    entry = tk.Entry(frame)
    entry.insert(0,setup_items[ff_mode][setting])
    entry.grid(row=row, column=col)
    widget_mapping[setting] = entry

# Function to create combobox widget
def create_tk_combobox(frame, value, row, col, setting, state="readonly"):
    combo = ttk.Combobox(frame, values=value, state=state)
    combo.grid(row=row, column=col)
    widget_mapping[setting] = combo
    
def validate_comboboxes(ok_button1, ok_button2):
    for key, widget in widget_mapping.items():
        if isinstance(widget, ttk.Combobox):
            if not widget.get():
                ok_button1.config(state=tk.DISABLED)
                ok_button2.config(state=tk.DISABLED)
                return
    ok_button1.config(state=tk.NORMAL)
    ok_button2.config(state=tk.NORMAL)

def _select_instrument_resource(setup_items, rm, ff_mode):
    # Button function to return the chosen resource and close the GUI
    def OK_press(mode):
        for (key, value) in widget_mapping.items():
            setup_items[mode][key] = value.get()
        print(setup_items[mode]) # DEBUG
        root.destroy()

    # List available resources
    available_resources = rm.list_resources()

    # Create a GUI to select the instrument
    root = tk.Tk()
    root.title("Select Instrument")
    root.geometry("640x400")  
    root.resizable(False, False)  

    # NOTEBOOK
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Create Frames for Settings
    motion_frame = ttk.Frame(notebook)
    notebook.add(motion_frame, text='Motion Controller')
    ff_frame = ttk.Frame(notebook)
    notebook.add(ff_frame, text='FieldFox')

    # Initialized row counters to zero and create labels
    row1 = 0 
    row2 = 0
    for (key, _) in setup_items[ff_mode].items():
        if key in motion_frame_settings:
            create_tk_labels(motion_frame, key, row1)
            row1 += 1
        else: 
            create_tk_labels(ff_frame, key, row2)
            row2 += 1
            
    # Reinitialize row counters to zero and create widgets
    row1 = 0
    row2 = 0
    for (key, _) in setup_items[ff_mode].items():
        if key == 'COM_PORT':
            ComPorts = [p.device for p in serial.tools.list_ports.comports()]
            create_tk_combobox(motion_frame, ComPorts, row1, 1, key)
            row1 +=1
        elif key == 'INSTR_ID':
            create_tk_combobox(ff_frame, available_resources, row2, 1, key)
            row2 += 1
        elif key == 'Enable_Gating':
            create_tk_combobox(ff_frame, [0, 1], row2, 1, key)
            row2 += 1
        else:
            if key in motion_frame_settings:
                create_tk_entry(motion_frame, row1, 1, key, ff_mode)
                row1 += 1
            else: 
                create_tk_entry(ff_frame, row2, 1, key, ff_mode)
                row2 += 1 

    ok_button1 = tk.Button(motion_frame, text="OK", command=lambda: OK_press(ff_mode), height=1, width=10, state=tk.DISABLED)
    ok_button1.grid(row=row1, column=0, columnspan=2, rowspan=2)
    ok_button2 = tk.Button(ff_frame, text="OK", command=lambda: OK_press(ff_mode), height=1, width=10, state=tk.DISABLED)
    ok_button2.grid(row=row2, column=0, columnspan=2, rowspan=2)
    
    # Bind the validation function to Combobox selection event
    for widget in widget_mapping.values():
        if isinstance(widget, ttk.Combobox):
            widget.bind("<<ComboboxSelected>>", lambda event, w=widget: validate_comboboxes(ok_button1, ok_button2))
            
    root.mainloop()