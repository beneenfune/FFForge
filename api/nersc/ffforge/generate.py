# generate.py
import argparse
import json

from ffforge_mlff import MLForceFieldMaker
from pymatgen.core.structure import Structure
from jobflow.managers.fireworks import flow_to_workflow
from fireworks import LaunchPad
from wf_helper import launch_step, load_workflow_specifications

# Main function to run GENERATE
def generate(workflow_dir):
    
    # 1 - Object processing
    # a - Get specifications from specifications json
    wf_spec = load_workflow_specifications(workflow_dir)
    workflow_id = wf_spec["workflow_id"]
    prefix = wf_spec["prefix"]
    max_structures = wf_spec["max_structures"]
    purpose = wf_spec["purpose"]
    # TODO: Resolve make() using is_molecular but i pass structure_type
    structure_filename = wf_spec["structure_filename"]

    # Conditionally add fields based on purpose
    if purpose == "DMA":
        structure_type = wf_spec["structure_type"]
    elif purpose == "Electrode depletion":
        atom_to_remove = wf_spec["atom_to_remove"]
    elif purpose == "Electrolyte analysis":
        electrolyte_atoms = wf_spec["electrolyte_atoms"]
    elif purpose == "Adsorption analysis":
        adsorbate_molecules = wf_spec["adsorbate_molecules"]

    structure_path = str(workflow_dir)+"/"+str(structure_filename)

    # b - Process structure file assuming its a pdb into Structure object
    structure = Structure.from_str(open(structure_path).read(), fmt="cif") # TODO: process wtv format to CIF depending on purpose, for now require CIF

    # 2 - Intialize the workflow
    
    # Create an instance of MLForceFieldMaker
    mlff_maker = MLForceFieldMaker()
    
    # TODO: eventually make workflow logic to process purpose-dependent conditions

    # Call make on the instance
    mlff_flow = mlff_maker.make(
        structure=structure,
        prefix=prefix,
        max_structures=max_structures,
        purpose=purpose
    )

    # Convert Flow to Workflow
    mlff_wf = flow_to_workflow(mlff_flow)

    # a - Add "workflow_id" from json in metadata of wf
    mlff_wf.metadata["workflow_id"] = workflow_id
    
    # 3 - Add worklflow to lpad
    
    # Intialize lpad (fworker and qadapter not needed here)
    mlff_lpad = LaunchPad.from_file('/global/homes/b/bfune/fw_config/my_launchpad.yaml')
    mlff_lpad.add_wf(mlff_wf) # Add wf to launchpad
    
    generate_fw_id = mlff_wf.root_fw_ids[0]
    run_fw_id = mlff_lpad.get_wf_by_fw_id(generate_fw_id).links[generate_fw_id][0]

    # 4 - Launch GENERATE
    launch_step(generate_fw_id, "generate", workflow_dir, workflow_id)

    # 5 - Launch RUN
    launch_step(run_fw_id, "run", workflow_dir, workflow_id)


# Parse command-line argument for workflow_dir
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run workflow generation.")
    parser.add_argument("workflow_dir", type=str, help="Path to the workflow directory.")
    args = parser.parse_args()
    generate(args.workflow_dir)