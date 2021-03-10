from flask import Flask
from flask_cors import CORS
from flask import request
from flask import render_template, redirect, send_file
import pandas as pd
import numpy as np
import os
from SB_support import *

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
    redirect('http://localhost:5000')
    new_df.to_csv('./metadata.csv')
    return send_file('./metadata.csv',
                  attachment_filename='metadata.csv',
                  as_attachment=True)
  elif routine == 'table':
    # Create new dataframe from SeaBASS data table
    new_df = pd.DataFrame(data.data)

    if time:
      # Creates a column that concatenates the hour and minute columns to XX:XX format
      new_df = new_df.assign(mod_minute = new_df["minute"].apply(str))
      new_df['mod_minute'] = new_df['mod_minute'].apply(lambda x: x.zfill(2))
      new_df = new_df.assign(complete_time = new_df["hour"].apply(str) + ":" + new_df["mod_minute"])
      new_df = new_df.drop(columns = "mod_minute")

    if date:
      # Creates a column that concatenates the day, month, and year to international standard DAY/MONTH/YEAR
      new_df = new_df.assign(complete_date = new_df["day"].apply(str) + "/" + new_df["month"].apply(str) + "/" + new_df["year"].apply(str))

    # Outputting file to user
    redirect('http://localhost:5000')
    new_df.to_csv('./data_table.csv')
    return send_file('./data_table.csv',
                  attachment_filename='data_table.csv',
                  as_attachment=True)

  else:
  # Return the original SeaBASS File
    redirect('http://localhost:5000')
    data.writeSBfile("./unmodified_data.sb")
    return send_file('./unmodified_data.sb',
                    attachment_filename='unmodified_data.sb',
                    as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
