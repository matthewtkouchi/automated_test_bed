/* OVERVIEW */
- The pyvisa library is used to communicate to the instrument drivers for the N9951A Field Fox using standardized SCPI commands.
- A serial object is used to communicate with an MM3000 motion controler via GPIB interface

The script works as follows:
- The parameters of the measurement are inputted by the user during setup. The setup parameters depends on whether the measurement is a NA or SA radiation pattern test. Normal SA tests can be done by setting the angle sweep to a single point.
- After establishing a connection to the FieldFox/Motion controller, the run_na or run_sa code is exectued to run the actual test and collect data. The collected data is stored in csv files and saved to a relevant path on the users local repository.
- After returning to the main function, saved csv data is read and organized into normalized and unnormalized dataframes
- Finally, the data is plotted on a popup window (with options to view normalized data and to hide certain tests from the plot)

/* HOW TO GET STARTED */
The user can run the auto.py executable to run the script.

For developers, all the required packages are listed in requirements.txt. To install the neccesary packages cd into the src directory from the terminal. 
Then run 'pip install -r requirements.txt'. After the installation is complete, the user may run the auto.py script and make any neccesary changes.