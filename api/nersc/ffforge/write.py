# write.py
import argparse

from wf_helper import launch_step, load_workflow_specifications
from fireworks import LaunchPad

# Main function to run WRITE
def write(workflow_dir):

    # Query root_fw of wf based on lpad
    wf_spec = load_workflow_specifications(workflow_dir)
    workflow_id = wf_spec["workflow_id"]

    # Initialize launch objects
    mlff_lpad = LaunchPad.from_file('/global/homes/b/bfune/fw_config/my_launchpad.yaml')

    # Query root_fw of wf based on lpad
    root_id_list = mlff_lpad.get_wf_ids(query={"metadata.workflow_id": str(workflow_id)})
    if not root_id_list:
        print(f"[ERROR] No workflows found with workflow_id {workflow_id}")
        return
    root_id = root_id_list[0]


    # Query states of wf
    wf_states = mlff_lpad.get_wf_by_fw_id(root_id).fw_states
    
    # Find fw_ids for 'READY' and 'WAITING'
    store_inputs_fw_id = None
    write_fw_id = None

    for fw_id, state in wf_states.items():
        if state == "READY" and store_inputs_fw_id is None:
            store_inputs_fw_id = fw_id
        elif state == "WAITING" and write_fw_id is None:
            write_fw_id = fw_id
    
    # Error handling if fw_ids are not found
    if store_inputs_fw_id is None:
        print("[ERROR] No Firework found in 'READY' state.")
        return
    if write_fw_id is None:
        print("[ERROR] No Firework found in 'WAITING' state.")
        return
    
    # Launch STORE_INPUTS
    launch_step(store_inputs_fw_id, "store_inputs", workflow_dir, workflow_id)

    # Launch WRITE
    launch_step(write_fw_id, "write", workflow_dir, workflow_id)
    
# Parse command-line argument for workflow_dir
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write workflow.")
    parser.add_argument("workflow_dir", type=str, help="Path to the workflow directory.")
    args = parser.parse_args()
    write(args.workflow_dir)