import os
import tkinter as tk
from tkinter import messagebox, ttk
import serial.tools.list_ports

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
        'Start_Angle': -86,
        'Stop_Angle': 86,
        'Step_Size': 2,
        'Span': 600e6,
        'Num_Points': 401,
        'Average_Passes': 1,
        'IFBW': 1e3,
    },
    'data': {
        'meas_foldername': "measurement-files",
        'meas_folderpath': None,
        'Normalized': 0,
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


def _select_instrument_resource(setup_items, rm, ff_mode):
    # Button function to return the chosen resource and close the GUI
    def OK_press(mode):
        setup_items[mode]['INSTR_ID'] = combo1.get()
        setup_items[mode]['COM_PORT'] = combo2.get()
        setup_items[mode]['Start_Angle'] = start.get()
        setup_items[mode]['Step_Size'] = step.get()
        setup_items[mode]['Stop_Angle'] = stop.get()
        setup_items[mode]['Span'] = span.get()
        setup_items[mode]['Center_Freq'] = center.get()
        setup_items[mode]['VBW'] = vbw.get()
        setup_items[mode]['RBW'] = rbw.get()

        # Fix for modes 
        print("Instrument ID is: " + setup_items[mode]['INSTR_ID'])
        print("Montion Controller Port is: " + setup_items[mode]['COM_PORT'])
        print("Start Angle Selected is: " + setup_items[mode]['Start_Angle'])
        print("Stop Angle Selected is: " + setup_items[mode]['Stop_Angle'])
        print("Step Size Selected is: " + setup_items[mode]['Step_Size'])
        print("Frequnecy Span is: " + setup_items[mode]['Span'])
        print("Center Frequnecy is: " + setup_items[mode]['Center_Freq'])
        print("VBW is: " + setup_items[mode]['VBW'])
        print("RBW is: " + setup_items[mode]['RBW'])

        root.destroy()

    # List available resources
    available_resources = rm.list_resources()
    
    # Create a GUI to select the instrument
    root = tk.Tk()
    root.title("Select Instrument")
    root.geometry("640x400")  
    root.resizable(False, False)  
    
    # If SA mode
    if ff_mode == 'sa':
        # Create a listbox and add availble resources
        tk.Label(root, text="INSTRUMENT ID:").grid(row=0)
        tk.Label(root, text="MOTION CONTROLLER PORT:").grid(row=1)
        tk.Label(root, text="START ANGLE:").grid(row=2)
        tk.Label(root, text="STEP SIZE:").grid(row=3)
        tk.Label(root, text="STOP ANGLE:").grid(row=4)
        tk.Label(root, text="FREQUENCY SPAN (Hz):").grid(row=5)
        tk.Label(root, text="CENTER FREQUENCY (Hz):").grid(row=6)
        tk.Label(root, text="VIDEO BANDWIDTH (Hz):").grid(row=7)
        tk.Label(root, text="RESOLUTION BANDWIDTH (Hz):").grid(row=8)
        
        combo1 = ttk.Combobox(values=available_resources, state="readonly")
        combo1.grid(row=0, column=1)
        ComPorts = [p.device for p in serial.tools.list_ports.comports()]
        combo2 = ttk.Combobox(values=ComPorts, state="readonly")
        combo2.grid(row=1, column=1)

        start = tk.Entry(root)
        start.insert(0,setup_items[ff_mode]['Start_Angle'])
        start.grid(row=2, column=1)
        step = tk.Entry(root)
        step.insert(0,setup_items[ff_mode]['Step_Size'])
        step.grid(row=3, column=1)
        stop = tk.Entry(root)
        stop.insert(0,setup_items[ff_mode]['Stop_Angle'])
        stop.grid(row=4, column=1)
        span = tk.Entry(root)
        span.insert(0,setup_items[ff_mode]['Span'])
        span.grid(row=5, column=1)
        center = tk.Entry(root)
        center.insert(0,setup_items[ff_mode]['Center_Freq'])
        center.grid(row=6, column=1)
        vbw = tk.Entry(root)
        vbw.insert(0,setup_items[ff_mode]['VBW'])
        vbw.grid(row=7, column=1)
        rbw = tk.Entry(root)
        rbw.insert(0, setup_items[ff_mode]['RBW'])
        rbw.grid(row=8, column=1)

        ok_button = tk.Button(root, text="OK", command=OK_press, height=1, width=10)
        ok_button.grid(row=9, column=0, columnspan=2, rowspan=2)
        
    # Else if NA mode
    elif ff_mode == 'na':
        # Create a listbox and add availble resources
        tk.Label(root, text="INSTRUMENT ID:").grid(row=0)
        tk.Label(root, text="MOTION CONTROLLER PORT:").grid(row=1)
        tk.Label(root, text="START ANGLE:").grid(row=2)
        tk.Label(root, text="STEP SIZE:").grid(row=3)
        tk.Label(root, text="STOP ANGLE:").grid(row=4)
        tk.Label(root, text="FREQUENCY SPAN (Hz):").grid(row=5)
        
        combo1 = ttk.Combobox(values=available_resources, state="readonly")
        combo1.grid(row=0, column=1)
        ComPorts = [p.device for p in serial.tools.list_ports.comports()]
        combo2 = ttk.Combobox(values=ComPorts, state="readonly")
        combo2.grid(row=1, column=1)
        
        start = tk.Entry(root)
        start.insert(0,setup_items[ff_mode]['Start_Angle'])
        start.grid(row=2, column=1)
        step = tk.Entry(root)
        step.insert(0,setup_items[ff_mode]['Step_Size'])
        step.grid(row=3, column=1)
        stop = tk.Entry(root)
        stop.insert(0,setup_items[ff_mode]['Stop_Angle'])
        stop.grid(row=4, column=1)
        span = tk.Entry(root)
        span.insert(0,setup_items[ff_mode]['Span'])
        span.grid(row=5, column=1)
        points = tk.Entry(root)
        points.insert(0,setup_items[ff_mode]['Num_Points'])
        points.grid(row=6, column=1)
        passes = tk.Entry(root)
        passes.insert(0,setup_items[ff_mode]['Average_Passes'])
        passes.grid(row=7, column=1)
        ifbw = tk.Entry(root)
        ifbw.insert(0,setup_items[ff_mode]['IFBW'])
        ifbw.grid(row=8, column=1)
        
        # Grid positioning may have to change
        ok_button = tk.Button(root, text="OK", command=OK_press, height=1, width=10)
        ok_button.grid(row=9, column=0, columnspan=2, rowspan=2)
        
    root.mainloop()