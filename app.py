"""
Web Application for Data Extraction of a SeaBASS File using Flask. 

Author: Neeka Sewnath, nsewnath@ufl.edu

"""

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
  time1 = request.form.get('time1')
  date1 = request.form.get('date1')
  time2 = request.form.get('time2')
  date2 = request.form.get('date2')

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
    redirect('http://localhost:5000')
    new_df.to_csv('./metadata.csv')
    return send_file('./metadata.csv',
                  attachment_filename='metadata.csv',
                  as_attachment=True)

  elif routine == 'table':
  # Create new dataframe from SeaBASS data table
    new_df = pd.DataFrame(data.data)

    if time1:
    # Creates a column that concatenates the hour and minute columns to XX:XX format
      new_df = new_df.assign(mod_minute = new_df["minute"].apply(str))
      new_df['mod_minute'] = new_df['mod_minute'].apply(lambda x: x.zfill(2))
      new_df = new_df.assign(complete_time = new_df["hour"].apply(str) + ":" + new_df["mod_minute"])
      new_df = new_df.drop(columns = "mod_minute")

    if date1:
    # Creates a column that concatenates the day, month, and year to international standard DAY/MONTH/YEAR
      new_df = new_df.assign(complete_date = new_df["day"].apply(str) + "/" + new_df["month"].apply(str) + "/" + new_df["year"].apply(str))

    # Outputting file to user
    redirect('http://localhost:5000')
    new_df.to_csv('./data_table.csv')
    return send_file('./data_table.csv',
                  attachment_filename='data_table.csv',
                  as_attachment=True)

  elif routine == 'modsb':
  # Outputs SeaBASS file with add-ons

    new_df = pd.DataFrame(data.data)

    if time2:
    # Creates a column that concatenates the hour and minute columns to XX:XX format
      new_df = new_df.assign(mod_minute = new_df["minute"].apply(str))
      new_df['mod_minute'] = new_df['mod_minute'].apply(lambda x: x.zfill(2))
      new_df = new_df.assign(complete_time = new_df["hour"].apply(str) + ":" + new_df["mod_minute"])
      new_df = new_df.drop(columns = "mod_minute")

      # Modifying headers
      fields = data.headers['fields']
      units = data.headers['units']
      new_field = fields + "," + "completed_time"
      new_unit = units + "," + "hh:mm"
      data.headers['fields']  = new_field
      data.headers['units'] = new_unit

    if date2:
    # Creates a column that concatenates the day, month, and year to international standard DAY/MONTH/YEAR
      new_df = new_df.assign(complete_date = new_df["day"].apply(str) + "/" + new_df["month"].apply(str) + "/" + new_df["year"].apply(str))

      # Modifying headers
      fields = data.headers['fields']
      units = data.headers['units']
      new_field = fields + "," + "completed_year"
      new_unit = units + "," + "dd/mm/yyyy"
      data.headers['fields']  = new_field
      data.headers['units'] = new_unit

    # Return the original SeaBASS File
    new_data = OrderedDict(new_df)
    data.data = new_data

    # Return the original SeaBASS File
    redirect('http://localhost:5000')
    data.writeSBfile("./seabass_w_extras.sb")
    return send_file('./seabass_w_extras.sb',
                    attachment_filename='seabass_w_extras.sb',
                    as_attachment=True)

#===========================================================================================================================================

if __name__ == '__main__':
    app.run(debug=True)
