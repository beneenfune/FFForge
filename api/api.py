from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

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
        return {'homepage': 'homepage yokoso'}

# Route for Demo Generator
class DemoGenerator(Resource):
    def get(self):
        return {'demo_gen': 'demo generator yokoso'}
    
    
    def post(self):

        # Parse input data
        parser = reqparse.RequestParser()
        parser.add_argument('structname', type=str, required=True, help='Name of Structure is required')
        parser.add_argument('starttemp', type=float, required=True, help='Starting Temperature is required')
        parser.add_argument('steptemp', type=float, required=True, help='Temperature Step is required')
        parser.add_argument('endtemp', type=float, required=True, help='Ending Temperature is required')
        args = parser.parse_args()

        # Get files from request
        infile = request.files['infile']
        datafile = request.files['datafile']
        slurmfile = request.files['slurmfile']


        # Save files to temp folder
        if not os.path.exists('temp'):
            os.makedirs('temp')
        
        infile_path = os.path.join('temp/', 'infile.txt')
        datafile_path = os.path.join('temp/', 'datafile.txt')
        slurmfile_path = os.path.join('temp/', 'slurmfile.slurm')

        infile.save(infile_path)
        datafile.save(datafile_path)
        slurmfile.save(slurmfile_path)

        # Process files using mlff_trj_gen
        structname = args['structname']
        starttemp = args['starttemp']
        steptemp = args['steptemp']
        endtemp = args['endtemp']

        # Example processing (replace with actual logic)
        response = {
            'structname': structname,
            'starttemp': starttemp,
            'steptemp': steptemp,
            'endtemp': endtemp,
            'message': f'Structure {structname} with temperature range {starttemp} to {endtemp} and step {steptemp} processed successfully.'
        }
        return jsonify(response), 200

"""
# Route for Demo
@app.route('/demo_generator')
def demo_gen():
    if request.method == 'POST':
        # First get data from user returns
        data_file = request.files['data_file']
        in_file = request.files['in_file']
        slurm_file = request.files['slurm_file']
        structure_name = request.args.get('structure_name', 'sample').replace(' ', '_')
        start_temp = float(request.args.get('start_temp', 0))
        end_temp = float(request.args.get('end_temp', 0))
        step_temp = float(request.args.get('step_temp', 0))

        # TODO: Check for edge cases before call function

        # Then call the function from demo_gen.py to get 
        # value of variables to send to HTML
        # path_to_zip = mlff_trj_gen()
        


        # Lastly, end the template by rendering the html 
        # and sending the variables over
        return render_template("demo_gen.html")
    return render_template("demo_gen.html")

"""

"""
Demo Input Generator Function

Parameters:
TODO descriptors of parameters
str structure_name :
str calc_dir :
list[float] temperature_range :
file in_file : 
file data_file :
file slurm_file :

Returns: 
str zip_path : path to zip file with input files inside 

def mlff_trj_gen(structure_name, calc_dir, start_temp, end_temp, step_temp, in_file, data_file, slurm_file):

    # Ensure the calc_dir exists (create if it does not exist)
    if not os.path.isdir(calc_dir):
        os.mkdir(calc_dir)
    
    # Change to the calculation directory
    os.chdir(calc_dir)
    
    # Create the structure directory
    os.mkdir(structure_name)
    os.chdir(structure_name)

    # Iterate in structure_name directory
    temperture_range = np.arange(start_temp, end_temp, step_temp)
    for temp in temperture_range:
        temp_dir = str(temp)

        os.mkdir(temp_dir)
        os.chdir(temp_dir)

        # TODO: what's passed in the file response, but subprocess uses the path
        # Copy files using subprocesses
        subprocess.call('cp {} in.{}'.format(in_file, structure_name), shell=True)
        subprocess.call('cp {} data.{}'.format(data_file, structure_name), shell=True)
        subprocess.call('cp {} {}.slurm'.format(slurm_file, structure_name), shell=True)

        # Replace placeholders in files
        subprocess.call("sed -i 's/master/{}/g' in.*".format(structure_name), shell=True)
        sed_string = "sed -i -e 's/master_jobname/{}/g ; s/master_prefix/{}/g ; s/master_temperature/{}/g' *.slurm".format(structure_name, structure_name, temp_dir)
        subprocess.call(sed_string, shell=True)
        os.chdir("../")
    ## ----------
        os.chdir("../")

    # After individual files are made, store in zip function to return 

    # subprocess.call('zip -r {}_files .'.format(structure_name), shell=True)
    try:
        # Using subprocess.run for better error handling and capturing output
        result = subprocess.run(
            ['zip', '-r', '{}_files.zip'.format(structure_name), '{}'.format(structure_name)],
            check=True,  # Raises CalledProcessError if the command exits with a non-zero status
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            text=True  # Decode the output as text (Python 3.7+)
        )
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        return None

    # Then, destroy all files in calculation directory for storage
    subprocess.call('rm -r {}'.format(structure_name))
    zip_path = '{}.{}'.format(CALC_ROOT, structure_name)
    return zip_path
"""

api.add_resource(Home, '/api/')
api.add_resource(DemoGenerator, '/api/demo_gen/')



# To start API
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)