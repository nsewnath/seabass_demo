"""

Web Application for Data Extraction of a NASA GSFC SeaBASS File using Flask. 

Author: Neeka Sewnath, nsewnath@ufl.edu

Note: SB_support.py is a SeaBASS Data Manipulation script that was written by Joel Scott (SAIC) and was downloaded from 
https://seabass.gsfc.nasa.gov/wiki/readsb_python

"""

#==========================================================================================================================================

from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template, redirect, send_file
import pandas as pd
import numpy as np
import os
from collections import OrderedDict
from SB_support import *

#==========================================================================================================================================

def mod_time(new_df):
  """Creates a column that concatenates the hour and minute columns to XX:XX format"""
  new_df = new_df.assign(mod_minute = new_df["minute"].apply(str))
  new_df['mod_minute'] = new_df['mod_minute'].apply(lambda x: x.zfill(2))
  new_df = new_df.assign(complete_time = new_df["hour"].apply(str) + ":" + new_df["mod_minute"])
  new_df = new_df.drop(columns = "mod_minute")
  return new_df

#==========================================================================================================================================

def mod_date(new_df):
  """Creates a column that concatenates the day, month, and year to international standard DAY/MONTH/YEAR"""
  new_df = new_df.assign(complete_date = new_df["day"].apply(str) + "/" + new_df["month"].apply(str) + "/" + new_df["year"].apply(str))
  return new_df

#==========================================================================================================================================

def return_csv(new_df, name):
  """Outputs csv file to user"""
  redirect('http://localhost:5000')
  new_df.to_csv('./' + name + '.csv')
  return send_file('./' + name + '.csv',
                    attachment_filename='./' + name + '.csv',
                    as_attachment=True)

#==========================================================================================================================================

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def routine():
  """Fetches SeaBASS file and exports selected data in CSV format"""

  # Gather routine request
  routine = request.form.get('routine')
  time = request.form.get('time')
  date = request.form.get('date')

  # Gather file
  file = request.files['file']
  filename = file.filename
  file.save(os.path.join("uploads", file.filename))
  path = os.path.join("uploads", file.filename)

  # Read SeaBASS File
  data = readSB(filename = path, no_warn = True)

  if routine == 'metadata':
  # Create new dataframe and assign ordered list keys and values as columns
    new_df = pd.DataFrame()
    new_df = new_df.assign(Labels = data.headers.keys())
    new_df = new_df.assign(Data = data.headers.values())

    # Outputting file to user
    name = "metadata"
    return return_csv(new_df, name)

  elif routine == 'table':
  # Create new dataframe from SeaBASS data table
    new_df = pd.DataFrame(data.data)

    if time:
      new_df = mod_time(new_df)

    if date:
      new_df = mod_date(new_df)

    # Outputting file to user
    name = "data_table"
    return return_csv(new_df, name)

  elif routine == 'modsb':
  # Outputs SeaBASS file with add-ons
    new_df = pd.DataFrame(data.data)

    if time:
      new_df = mod_time(new_df)

      # Modifying headers
      fields = data.headers['fields']
      units = data.headers['units']
      data.headers['fields']  = fields + "," + "completed_time"
      data.headers['units'] = units + "," + "hh:mn"

    if date:
      new_df = mod_date(new_df)

      # Modifying headers
      fields = data.headers['fields']
      units = data.headers['units']
      data.headers['fields']  = fields + "," + "completed_year"
      data.headers['units'] = units + "," + "dd/mm/yyyy"

    # Return the original SeaBASS File
    new_data = OrderedDict(new_df)
    data.data = new_data

    # Return the original SeaBASS File
    data.writeSBfile("./seabass_w_extras.sb")
    return send_file('./seabass_w_extras.sb',
                    attachment_filename='seabass_w_extras.sb',
                    as_attachment=True)

#===========================================================================================================================================

if __name__ == '__main__':
    app.run(debug=True)
