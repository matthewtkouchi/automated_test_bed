import pyvisa
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import Checkbutton
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from helper import run_na, run_sa, read_csv_files, get_axis_data, plot_data, onNormalizedClick, toggle_display
from common import *

# import user defined functions
from setup import _get_csv_folder_path, _get_ff_mode, _select_instrument_resource
#from csv_files import rename_csv_files

# import user defined data structures
from setup import setup_items

# Initialize the total paths list
Total_Paths = []

# Initialize plot variables
Normalized_Data = []
Unnormalized_Data = []

# Select the FieldFox mode (SA or NA)
ff_mode = _get_ff_mode()

# Connect with the FieldFox
rm = pyvisa.ResourceManager()  
_select_instrument_resource(setup_items, rm, ff_mode)
my_instrument = rm.open_resource(setup_items[ff_mode]['INSTR_ID'])

# Configure the serial connection to the motion controller
ser = serial.Serial(
    port=setup_items[ff_mode]['COM_PORT'],
    baudrate=9600,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Run the Radiation Pattern Measurement for the NA or SA
if ff_mode == 'sa':
    run_na(setup_items, my_instrument, ser, ff_mode, Total_Paths)
elif ff_mode == 'na':
    run_sa(setup_items, my_instrument, ser, ff_mode, Total_Paths)

# Create a tkinter window
root = tk.Tk()
root.title("Matplotlib in Tkinter")
Normalized = tk.IntVar(root)

# Read all csv files from the Total_Paths and populate the Unnormalized_Data and Normalized_Data
read_csv_files(Total_Paths, Unnormalized_Data, Normalized_Data)

# Get y-axis (power) data for plotting
x_data, y_data_unnorm, y_data_norm = get_axis_data(Unnormalized_Data, Normalized_Data)

# Create a matplotlib figure
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Create a canvas to embed the pyplot figure in the tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Create toggle buttons for each item in column_data
toggle_buttons = []
toggle_button = Checkbutton(root, text="Normalized", variable=Normalized, onvalue = 1, offvalue = 0, command=onNormalizedClick(Normalized))
toggle_buttons.append(toggle_button)
toggle_button.pack()

for column, data_info in y_data_unnorm.items():
    var = tk.BooleanVar(value=data_info["display"])  # Initialize with the correct value
    toggle_button = Checkbutton(root, text=column, variable=var,
                                command=lambda col=column: toggle_display(column, y_data_unnorm, y_data_norm, ax, canvas, x_data))
    toggle_buttons.append(toggle_button)
    toggle_button.pack()

# Call the plot_data function to plot the data
plot_data(ax, canvas, x_data, y_data_unnorm, y_data_norm)

# Start the tkinter main loop
root.mainloop()