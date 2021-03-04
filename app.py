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
def metadata():
  """Fetches metadata from SeaBASS file and exports as CSV"""

  # Gather specified request
  metadata = request.form.get('metadata')

  # Gather file
  file = request.files['file']
  filename = file.filename
  file.save(os.path.join("uploads", file.filename))
  path = os.path.join("uploads", file.filename)

  # Read SeaBASS File
  data = readSB(filename = path, no_warn = True)

  if metadata:
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

  # This can be used if a SeaBASS file needs to be returned
  #data.writeSBfile("./new_data.sb")
  #return send_file('./new_data.sb',
  #                attachment_filename='new_data.sb',
  #                as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
