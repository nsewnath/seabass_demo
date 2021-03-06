# SeaBASS Data Product Demo
This is a small demo of using a web application interface to extract data from a SeaBASS file. Other functions could be added to this in the future. 

SB_support.py from https://seabass.gsfc.nasa.gov/wiki/readsb_python

# Inputs
SeaBASS files only. 
Test file from https://seabass.gsfc.nasa.gov/archive/BIGELOW/BALCH/AL9807/archive

# Outputs 
CSV files for metadata and data table (depending on user selection). If no routine is selected then the original SeaBASS file will be returned unmodified. 

# How to Run: 
1. Navigate to the project folder in Command Prompt/Terminal.
2. Make sure you have all of the dependencies installed (namely Pandas and Flask)
3. Run the python file [app.py](http://app.py) (you can use command python app.py).
4. Navigate to [http://localhost:5000/](http://localhost:5000/).
5. Select a SEABass file and specify routine. 

