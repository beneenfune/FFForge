# wf_helper.py
import os
import json
from fireworks.core.rocket_launcher import launch_rocket
from fireworks.queue.queue_launcher import launch_rocket_to_queue
from fireworks import LaunchPad, FWorker
from fireworks.utilities.fw_serializers import load_object_from_file

# Function to create a directory and run the workflow step inside it
def launch_step(fw_id, step_name, workflow_dir, workflow_id):
    mlff_lpad = LaunchPad.from_file('/global/homes/b/bfune/fw_config/my_launchpad.yaml')
    step_dir = os.path.join(workflow_dir, f"{step_name}_{workflow_id}")

    # Ensure the directory exists
    os.makedirs(step_dir, exist_ok=True)

    # Store the current working directory
    original_dir = os.getcwd()

    try:
        # Change to step directory
        os.chdir(step_dir)

        # Launch the job to login node
        launch_rocket(mlff_lpad, fw_id=fw_id)
    finally:
        # Return to original directory
        os.chdir(original_dir)

# Function to create a directory and run the workflow step inside it
def launch_step_to_queue(fw_id, step_name, workflow_dir, workflow_id):
    mlff_lpad = LaunchPad.from_file('/global/homes/b/bfune/fw_config/my_launchpad.yaml')
    mlff_fworker = FWorker.from_file('/global/homes/b/bfune/fw_config/my_fworker.yaml')
    mlff_qadapter = load_object_from_file("/global/homes/b/bfune/fw_config/my_qadapter.yaml")

    step_dir = os.path.join(workflow_dir, f"{step_name}_{fw_id}_{workflow_id}")

    # Ensure the directory exists
    os.makedirs(step_dir, exist_ok=True)

    # Store the current working directory
    original_dir = os.getcwd()

    try:
        # Change to step directory
        os.chdir(step_dir)

        # Launch job to compute node
        launch_rocket_to_queue(
            mlff_lpad,
            mlff_fworker,
            mlff_qadapter,
            reserve=True,
            launcher_dir=step_dir,
            strm_lvl="DEBUG",
            fw_id=fw_id) 

    finally:
        # Return to original directory
        os.chdir(original_dir)

# Function to load workflow specifications
def load_workflow_specifications(workflow_dir):

    # Find the workflow specification JSON file
    json_filename = [f for f in os.listdir(workflow_dir) if f.startswith("wf_specifications") and f.endswith(".json")]
    if not json_filename:
        raise FileNotFoundError("Workflow specification JSON file not found in the workflow directory.")

    json_path = os.path.join(workflow_dir, json_filename[0])

    # Load JSON data
    with open(json_path, 'r') as file:
        return json.load(file)
    
