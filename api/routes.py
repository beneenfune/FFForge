from __init__ import api

from flask import request, send_from_directory, url_for, jsonify, make_response
from flask_restful import Resource, reqparse
from utils.demo import mlff_trj_gen, remove_dir, zip_dir
from utils.sfapi import upload_file, create_directory_on_login_node, get_status, cat_file, get_task, get_all_lpad_wflows, remove_file, recursively_rm_dir, run_worker_step, get_lpad_wf
from utils.preprocessing import generate_hash
from utils.db import ffforge_collection, users_collection, workflows_collection, update_workflow_status
from fetcher import run_fetcher, stop_fetcher
from models.workflowModel import create_workflow_entry  # Import model function

from bson.objectid import ObjectId
import os
import subprocess
import asyncio
import numpy as np
import json
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

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
        return {'text': 'welcome to text input page', 'test-text':'H2o'}
    
    def post(self):

        # Access request data
        smiles = request.get('smiles_string')
        print("SMILES string processed in Flask API")

        return {
            'smiles_string': smiles 
        }
    
# Route for File Input Page
class FileInput(Resource):
    def get(self, path):
        return send_from_directory('static', path)
    
    def post(self):
        # Create new files in temp directory
        if not os.path.exists('static'):
            os.makedirs('static')

        # Process and save the structure files
        structure_file = request.files.get('structureFile')

        # Initialize the file path variable
        structure_file_path = ""

        # Save file to the new file in the static directory
        if structure_file:
            try:
                original_filename = structure_file.filename
                prefix = os.path.splitext(original_filename)[0]
                extension = os.path.splitext(original_filename)[1]
                
                # Generate a unique directory name
                hashed_directory_name = generate_hash()

                # Create a directory in Perlmutter
                try:
                    root_dir = os.getenv("ROOT_DIR") + "/sf_api_implementing"
                    if not root_dir:
                        raise EnvironmentError("ROOT_DIR environment variable not set.")
                    
                    new_directory = create_directory_on_login_node("perlmutter", root_dir, directory_name=hashed_directory_name)
                    if not new_directory:
                        return {'error': "Failed to create directory on Perlmutter. Please check configuration and try again."}, 500

                except Exception as e:
                    return {'error': f"Failed to create directory on Perlmutter: {str(e)}"}, 500
                
                print("New directory on Perlmutter: " + new_directory)

                # Construct the new filename
                new_filename = f"{prefix}_{hashed_directory_name}{extension}"
                structure_file_path = os.path.join('static', new_filename)
                
                # Save the file with the new filename
                structure_file.save(structure_file_path)
            except Exception as e:
                return {'error': f"Failed to save structure file: {str(e)}"}, 500
            
            print("The structure_file_path is " + structure_file_path)
            full_path = url_for('static', filename=new_filename, _external=True)

            # Use sfapi to upload the file to the supercomputer
            try:
                # Run the asynchronous upload_file function
                asyncio.run(upload_file(structure_file_path, new_directory))
            except Exception as e:
                return {'error': f"Failed to upload file to Perlmutter: {str(e)}"}, 500

            return jsonify ({
                "message": "File uploaded and saved to local backend and Perlmutter.",
                'structure_path' : full_path
            })
        else:
            return jsonify({"error": "No file uploaded."}), 400

# Route for Design GUI Page
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

# Route for Workspace Page
class Workspace(Resource):
    def get(self):
        return {'workspace': 'welcome to a random workspace'}

class Test_SFAPI_Connection(Resource):

    # Get NERSC status: for testing connection to NERSC purposes
    def get(self):
        status_data = asyncio.run(get_status())
        return status_data

    # Cat a file in NERSC: for testing Run Command ability purposes
    def post(self):
        root_dir = os.getenv("ROOT_DIR") + "/sf_api_implementing"
        file_name = "run_command_file.txt"
        cat_results = cat_file(root_dir, file_name)
        cat_results["next_step"] = "please run task_id in 'Get Task from ID endpoint' to confirm cat"
        return { "cat_result": cat_results }

class Test_SFAPI_Get_Task(Resource):
    """API Resource to fetch task outputs."""

    def get(self, task_id):
        max_retries = int(request.args.get("max_retries", 10))
        delay = int(request.args.get("delay", 5))
        result = get_task(task_id, max_retries=max_retries, delay=delay)
        
        # Check if 'result' exists in task data
        raw_result = result.get("result")  # Get raw result string
        if not raw_result:
            return {"error": "No result found for the given task."}, 404

        # Parse raw_result if it's a string
        if isinstance(raw_result, str):
            try:
                result_data = json.loads(raw_result)
            except json.JSONDecodeError as e:
                print(f"[ERROR] JSON decode error: {str(e)}")
                return {"error": "Failed to parse task result."}, 500
        else:
            result_data = raw_result  # It's already a dictionary

        # Now check if "output" exists in parsed result_data
        if "output" not in result_data or result_data["output"] is None:
            return {"error": "No output found in task result."}, 404

        # Extract and parse the output if needed
        output_data = result_data["output"]

        # Check if output is a string that needs parsing
        if isinstance(output_data, str):
            try:
                output_data = json.loads(output_data)
            except json.JSONDecodeError:
                pass  # Leave it as a string if it's not valid JSON

        # Validate output format (string, list, or dict expected)
        if not isinstance(output_data, (str, list, dict)):
            return {"error": "Unexpected output format."}, 500

        return output_data, 200



class Test_SFAPI_Wflows(Resource):
    # Get a launchpad workflow 
    def get(self):
        workflow_id = request.form.get('workflow_id')
        query_filter = request.form.get('query_filter')
        return get_lpad_wf(workflow_id, query_filter)

    # Get all launchpad workflows
    def post(self):
        return get_all_lpad_wflows()
        
class Test_WorkflowSubmission(Resource):
    def post(self):
        worker_step = request.form.get('worker_step')
        workflow_id = request.form.get('workflow_id')
        return run_worker_step(worker_step, workflow_id)

class Test_UpdateStatus(Resource):
    def post(self):
        workflow_id = request.form.get('workflow_id')
        new_status = request.form.get('new_status')
        return update_workflow_status(new_status, workflow_id)
    
class WorkflowSubmission(Resource):
    def post(self):
        structure_file_path = None
        json_file_path = None
        try:
            # Extract base fields
            data = {
                "prefix": request.form.get('prefix'),
                "max_structures": int(request.form.get('max_structures')),
                "purpose": request.form.get('purpose'),
                "use_active_learning": request.form.get('use_active_learning'),
            }

            # Conditionally extract additional fields
            if data["purpose"] == "DMA":
                data["structure_type"] = request.form.get("structure_type")
            elif data["purpose"] == "Electrode depletion":
                data["atom_to_remove"] = request.form.get("atom_to_remove")
            elif data["purpose"] == "Electrolyte analysis":
                data["electrolyte_atoms"] = request.form.get("electrolyte_atoms")
            elif data["purpose"] == "Adsorption analysis":
                data["adsorbate_molecules"] = request.form.get("adsorbate_molecules")

            # Create workflow entry
            workflow_entry = create_workflow_entry(data)
            workflow_id = workflows_collection.insert_one(workflow_entry).inserted_id

            # Ensure a file is uploaded
            if 'structure_file' not in request.files or request.files['structure_file'].filename == '':
                return {'error': 'A structure file is required for this workflow submission.'}, 400
            structure_file = request.files.get('structure_file')

            # Create 'static' directory if it doesn't exist
            if not os.path.exists('static'):
                os.makedirs('static')
                
            original_filename = structure_file.filename
            prefix = os.path.splitext(original_filename)[0]
            extension = os.path.splitext(original_filename)[1]

            # Use workflow_id as name of directory to put file in
            workflow_dir_name = str(workflow_id)

            # Create a directory in Perlmutter
            root_dir = os.getenv("ROOT_DIR")
            if not root_dir:
                raise EnvironmentError("ROOT_DIR environment variable not set.")
            
            new_directory = create_directory_on_login_node("perlmutter", root_dir + "/workflows", workflow_dir_name)            
            if not new_directory:
                return {'error': "Failed to create directory on Perlmutter."}, 500

            # Construct the new structure file name
            new_filename = f"{prefix}_{workflow_id}{extension}"
            structure_file_path = os.path.join('static', new_filename)
            structure_file.save(structure_file_path) # Save the structure file locally

            # Create JSON file containing workflow specifications
            json_filename = f"wf_specifications_{prefix}_{workflow_id}.json"
            json_file_path = os.path.join('static', json_filename)


            # Base specification
            wf_specification = {
                "workflow_id": str(workflow_id),
                "prefix": data["prefix"],
                "max_structures": data["max_structures"],
                "purpose": data["purpose"],
                "use_active_learning": data["use_active_learning"],
                "structure_filename": new_filename  # Store reference to the structure file
            }

            # Conditionally add fields based on purpose
            if data["purpose"] == "DMA":
                wf_specification["structure_type"] = data["structure_type"]
            elif data["purpose"] == "Electrode depletion":
                wf_specification["atom_to_remove"] = data["atom_to_remove"]
            elif data["purpose"] == "Electrolyte analysis":
                wf_specification["electrolyte_atoms"] = data["electrolyte_atoms"]
            elif data["purpose"] == "Adsorption analysis":
                wf_specification["adsorbate_molecules"] = data["adsorbate_molecules"]


            # Write JSON data to file
            with open(json_file_path, 'w') as json_file:
                json.dump(wf_specification, json_file, indent=4)

            # Upload files to Perlmutter
            try:
                asyncio.run(upload_file(structure_file_path, new_directory)) # Upload structure file
                asyncio.run(upload_file(json_file_path, new_directory)) # Upload workflow specification file

            except Exception as e:
                return {'error': f"Failed to upload files to Perlmutter: {str(e)}"}, 500
            
            # Update mongoDB wf entry
            new_status = "generating runs"
            update_workflow_status(new_status, str(workflow_id))

            return {
                "message": "Workflow submitted and files uploaded successfully!",
                "workflow_id": str(workflow_id),
            }, 201  # HTTP 201 Created

        except Exception as e:
            return {"error": str(e)}, 400  # HTTP 400 Bad Request
        
        finally:
            # Remove local files if they exist
            if structure_file_path and os.path.exists(structure_file_path):
                os.remove(structure_file_path)
            if json_file_path and os.path.exists(json_file_path):
                os.remove(json_file_path)
            
            # Start a fetcher for this workflow
            # run_fetcher(workflow_id)



class WorkflowDeletion(Resource):
    def delete(self, workflow_id):
        try:
            # Attempt to delete the workflow entry from MongoDB
            result = workflows_collection.delete_one({"_id": ObjectId(workflow_id)})
            
            # If no document was deleted, return a 404 response indicating workflow not found
            if result.deleted_count == 0:
                return {"message": "Workflow not found"}, 404  # Not Found
            
            try: 
                # Retrieve the root directory path from environment variables
                root_dir = os.getenv("ROOT_DIR")
                if not root_dir:
                    raise EnvironmentError("ROOT_DIR environment variable not set.")
                
                # Construct the full path of the workflow directory on Perlmutter
                workflow_dir = root_dir + "/workflows/"+ workflow_id
                
                # Attempt to remove the workflow directory from Perlmutter
                rm_dir = recursively_rm_dir(workflow_dir)
                if not rm_dir:
                    return {'error': "Failed to remove workflow directory on Perlmutter. Please check configuration and try again."}, 500
            except Exception as e:
                return {'error': f"Failed to upload file to Perlmutter: {str(e)}"}, 500
            
            return {"message": "Workflow deleted from database and Perlmutter successfully"}, 200  # Success

        except Exception as e:
            return {"error": str(e)}, 400  # Bad Request
        
class Test_Remove_File(Resource):
    # Remove a file in NERSC
    def post(self):
        
        sub_dir = request.form.get('sub_dir')
        file_name = request.form.get('file_name')
        root_dir = os.getenv("ROOT_DIR")
        target_dir = root_dir + sub_dir
        rm_results = remove_file(target_dir, file_name)
        rm_results["next_step"] = "please run task_id in 'Get Task from ID endpoint' to confirm rm"
        return { "rm_results": rm_results }

class WorkflowsGetAll(Resource):
    def get(self):
        try:
            # Fetch all workflows from the collection
            workflows = list(workflows_collection.find({}, {"_id": 1, "prefix": 1, "max_structures": 1, "purpose": 1, "status": 1, "created_at": 1}))
            
            # Convert ObjectId to string for JSON serialization
            for workflow in workflows:
                workflow["_id"] = str(workflow["_id"])
                workflow["created_at"] = workflow["created_at"].isoformat()  # Convert datetime to string
            
            return jsonify({"workflows": workflows})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500        

class StartFetcher(Resource):
    """
    API to start fetcher for a workflow.
    """

    def post(self):
        workflow_id = request.form.get('workflow_id')

        if not workflow_id:
            return {"error": "workflow_id is required."}, 400

        run_fetcher(workflow_id)
        return {"message": f"Fetcher started for workflow {workflow_id}."}, 200

class StopFetcher(Resource):
    """
    API to stop a running fetcher.
    """

    def post(self):
        workflow_id = request.form.get('workflow_id')

        if not workflow_id:
            return {"error": "workflow_id is required."}, 400

        stop_fetcher(workflow_id)
        return {"message": f"Fetcher stopped for workflow {workflow_id}."}, 200

# -------------------------------------------------------------------------
# Dummy structure endpoints
from flask import abort
from bson.objectid import ObjectId
from utils.db import dummy_structures_collection

# ...existing code...

class StructureListAPI(Resource):
    def post(self):
        """Create a Structure using form-data"""
        name = request.form.get("name")
        smiles = request.form.get("smiles")
        if not name or not smiles:
            return {"error": "Both 'name' and 'smiles' fields are required."}, 400
        structure = {
            "name": name,
            "smiles": smiles
        }
        result = dummy_structures_collection.insert_one(structure)
        # Instead of returning the structure dict (which lacks the id), return this:
        return {
            "id": str(result.inserted_id),
            "name": name,
            "smiles": smiles
        }, 201

    def get(self):
        """Get All Structures"""
        structures = []
        for doc in dummy_structures_collection.find():
            structures.append({
                "id": str(doc["_id"]),
                "name": doc.get("name"),
                "smiles": doc.get("smiles")
            })
        return structures, 200

class StructureDetailAPI(Resource):
    def get(self, structure_id):
        """Get a Specific Structure"""
        doc = dummy_structures_collection.find_one({"_id": ObjectId(structure_id)})
        if not doc:
            abort(404)
        return {
            "id": str(doc["_id"]),
            "name": doc.get("name"),
            "smiles": doc.get("smiles")
        }, 200

    def put(self, structure_id):
        """Update a Structure using form-data"""
        name = request.form.get("name")
        smiles = request.form.get("smiles")
        update = {}
        if name is not None:
            update["name"] = name
        if smiles is not None:
            update["smiles"] = smiles
        if not update:
            return {"error": "At least one of 'name' or 'smiles' must be provided."}, 400
        result = dummy_structures_collection.find_one_and_update(
            {"_id": ObjectId(structure_id)},
            {"$set": update},
            return_document=True
        )
        if not result:
            abort(404)
        # Convert ObjectId to string before returning!
        return {
            "id": str(result["_id"]),
            "name": result.get("name"),
            "smiles": result.get("smiles")
        }, 200

    def delete(self, structure_id):
        """Delete a Structure"""
        result = dummy_structures_collection.delete_one({"_id": ObjectId(structure_id)})
        if result.deleted_count == 0:
            abort(404)
        return {"message": f"Structure {structure_id} deleted successfully."}, 200

# Add dummy structure endpoints to app
api.add_resource(StructureListAPI, '/api/dummy/structures')
api.add_resource(StructureDetailAPI, '/api/dummy/structures/<string:structure_id>')

# -------------------------------------------------------------------------

# Add fetcher endpoints
api.add_resource(StartFetcher, "/api/v1/start_fetcher")
api.add_resource(StopFetcher, "/api/v1/stop_fetcher")

# V0
api.add_resource(Home, '/api/')
api.add_resource(DemoGenerator, '/api/demo_gen/')
api.add_resource(DemoDownload, '/static/<path:path>')
api.add_resource(Landing, '/api/landing/')
api.add_resource(TextInput, '/api/text-input/')
api.add_resource(FileInput, '/api/file-input/')
# api.add_resource(Ketcher, '/api/edit/')
api.add_resource(Visualize, '/api/visualize')
api.add_resource(TempFileHandler, '/api/getfile/<string:filename>')
api.add_resource(Workspace, '/api/workspace')


# V1
api.add_resource(Test_SFAPI_Connection, '/api/v1/sfapi/connect')
api.add_resource(Test_SFAPI_Get_Task, '/api/v1/sfapi/get/task/<int:task_id>')
api.add_resource(Test_SFAPI_Wflows, '/api/v1/sfapi/test/wflows')
api.add_resource(Test_Remove_File, "/api/v1/sfapi/file/delete/")
api.add_resource(Test_WorkflowSubmission, "/api/v1/sfapi/test/workflow/submit")
api.add_resource(Test_UpdateStatus, "/api/v1/sfapi/test/update/workflow")
api.add_resource(WorkflowSubmission, '/api/v1/workflow/submit')
api.add_resource(WorkflowDeletion, "/api/v1/workflow/delete/<string:workflow_id>")
api.add_resource(WorkflowsGetAll, "/api/v1/workflow/all")
api.add_resource(StartFetcher, "/api/v1/start_fetcher", endpoint="start_fetcher")
api.add_resource(StopFetcher, "/api/v1/stop_fetcher", endpoint="stop_fetcher")



