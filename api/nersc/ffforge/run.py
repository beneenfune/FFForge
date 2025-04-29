# run.py
import argparse

from wf_helper import launch_step, launch_step_to_queue, load_workflow_specifications
from fireworks import LaunchPad

# Main function to run RUN
def run(workflow_dir):

    # Query root_fw of wf based on lpad
    wf_spec = load_workflow_specifications(workflow_dir)
    workflow_id = wf_spec["workflow_id"]

    # Initialize launch objects
    mlff_lpad = LaunchPad.from_file('/global/homes/b/bfune/fw_config/my_launchpad.yaml')

    # Query root_fw of wf based on lpad
    root_id_list = mlff_lpad.get_wf_ids(query={"metadata.workflow_id": str(workflow_id)})
    root_id = root_id_list[0]

    # Query states of wf
    wf_states = mlff_lpad.get_wf_by_fw_id(root_id).fw_states
    wf_ready_states = {fw_id: state for fw_id, state in wf_states.items() if state=='READY'}

    # Launch all READY fws
    for fw_id, state in wf_ready_states.items():

        # Submit job to queue
        launch_step_to_queue(fw_id, "static", workflow_dir, workflow_id)


# Parse command-line argument for workflow_dir
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run workflow generation.")
    parser.add_argument("workflow_dir", type=str, help="Path to the workflow directory.")
    args = parser.parse_args()
    run(args.workflow_dir)