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
    
# Route for SMILES Text input Page
class TextInput(Resource):
    def get(self):
        return {'text': 'welcome to text input page'}
    
# Route for File Input Page
class FileInput(Resource):
    def get(self):
        return {'land': 'welcome to file input page'}
    
# Route for File Input Page
class Ketcher(Resource):
    def get(self):
        return {'design': 'welcome to the design page'}
    

class TempFileHandler(Resource):
    def get(self, filename):
        # parser = reqparse.RequestParser()
        # parser.add_argument('filename', type=str, help='The file name that you wish to retrieve from the temp directory')
        # args = parser.parse_args()

        # TODO - Add error handling for file not found
        # TODO - Prevent directory traversal attacks by changing how this is done
        with open(f'temp/{filename}', 'r') as f:
            output = f.read()
        
        return {"content": output}
    
class Visualize(Resource):
    def get(self):
        return {'visualize': 'welcome to the visualization page'}

    def post(self):
        # Parse the input data
        parser = reqparse.RequestParser()
        parser.add_argument('molfile', type=str, help='The molfile input (v2000)')
        args = parser.parse_args()

        # Find an unused filename from molfile1.mol, molfile2.mol, ...
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        i = 1
        while os.path.exists(f'temp/molfile{i}.mol'):
            i += 1

        # Save the molfile to a new file in the temp directory
        with open(f'temp/molfile{i}.mol', 'w') as f:
            f.write(args['molfile'])

        # Run the scripts to generate output files

        # Read output files and return the data
        with open(f'temp/molfile{i}.mol', 'r') as f:
            output = f.read()

        # Delete all the temp files created in the process
        os.remove(f'temp/molfile{i}.mol')

        return {'output': output}

api.add_resource(Home, '/api/')
api.add_resource(DemoGenerator, '/api/demo_gen/')
api.add_resource(DemoDownload, '/static/<path:path>')
api.add_resource(Landing, '/api/landing/')
api.add_resource(TextInput, '/api/text-input/')
api.add_resource(FileInput, '/api/file-input/')
api.add_resource(Ketcher, '/api/edit/')
api.add_resource(Visualize, '/api/visualize')
api.add_resource(TempFileHandler, '/api/getfile/<string:filename>')




# To start API
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)