from flask import Flask, jsonify, request, send_from_directory, send_file, url_for
from flask_restful import Resource, Api, reqparse
from demo import mlff_trj_gen, zip_dir, remove_dir

import os
import subprocess
import requests
import numpy as np


app = Flask(__name__)
api = Api(app)

# For CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# Route for Home page
class Home(Resource):
    def get(self):
        return {'homepage': 'welcome to homepage'}

# Route for Demo Generator
class DemoGenerator(Resource):
    def get(self):
        return {'demo_gen': 'welcome to demo generator'}
    
    def post(self):

        # Access form data
        structname = request.form.get('structname')
        starttemp = float(request.form.get('starttemp'))
        steptemp = float(request.form.get('steptemp'))
        endtemp = float(request.form.get('endtemp'))
        
        # Create new files in temp directory
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        temp_dir = os.path.join('temp')

        # Process and save the uploaded files
        infile = request.files.get('infile')
        datafile = request.files.get('datafile')
        slurmfile = request.files.get('slurmfile')

        # Save file args to the new files in the temp directory
        if infile:
            infile_path = os.path.join('temp', 'infile.txt')
            infile.save(infile_path)
        if datafile:
            datafile_path = os.path.join('temp', 'datafile.txt')
            datafile.save(datafile_path)
        if slurmfile:
            slurmfile_path = os.path.join('temp', 'slurmfile.slurm')
            slurmfile.save(slurmfile_path)
        
        # Ensure the calculations directory exists
        if not os.path.exists('calculations'):
            os.makedirs('calculations')
        
        calc_dir = os.path.join('calculations')

        # Create temperature range
        temp_range = np.arange(starttemp, endtemp, steptemp)

        # Process files using mlff_trj_gen to generate output files
        mlff_trj_gen(structname, calc_dir, temp_range, infile_path, datafile_path,slurmfile_path)

        # Zip recursively
        try:
            zip_path = zip_dir(calc_dir, './demo')
        except Exception as e:
            return {'error': f"Failed to create zip file: {str(e)}"}, 500

        # Remove temp and calculations if zip was successful, otherwise error
        try:
            remove_dir(calc_dir)
            remove_dir(temp_dir)
        except Exception as e:
            return {'error': f"Failed to remove directories: {str(e)}"}, 500

        # Ensure the calculations directory exists
        if not os.path.exists('calculations'):
            os.makedirs('calculations')
        
        subprocess.call('mv {} static/'.format(zip_path), shell=True)
        full_zip_path = url_for('static', filename='demo.zip', _external=True)

        return {
            'zPath': full_zip_path 
        }

# Route for Demo Generator
class DemoDownload(Resource):
    def get(self, path):
        return send_from_directory('static', path)
    
# Route for Landing Page
class Landing(Resource):
    def get(self):
        return {'land': 'welcome to landing page'}

api.add_resource(Home, '/api/')
api.add_resource(DemoGenerator, '/api/demo_gen/')
api.add_resource(DemoDownload, '/static/<path:path>')
api.add_resource(Landing, '/api/landing/')




# To start API
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)