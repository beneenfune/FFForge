from fireworks import LaunchPad
from jobflow.managers.fireworks import flow_to_workflow
from fireworks.queue.queue_launcher import rapidfire, launch_rocket_to_queue

# TODO: from flow import ForgeForceFieldsMaker
# the import: from atomate2.vasp.flows.mlff import MLForceFieldMaker

mlff_flow = MLForceFieldMaker().make(structure, 300)

mlff_wf = flow_to_workflow(mlff_flow)

lpad = LaunchPad.auto_load()
lpad.add(mlff_wf)

# (on terminal): qlaunch -r rapidfire
# python way of runnign qlaunch look at -> def launch_rocket_to_queueg