# watcher.py

import threading
import pymongo
from bson import ObjectId
from pymongo import MongoClient
from utils.sfapi import run_worker_step
from utils.db import  workflows_collection, update_workflow_status
import os


# Status-worker mapping
STATUS_ACTIONS = {
    "generating runs": "generate",
    "launching to queue": "run",
    "writing": "write",
}

def handle_status_change(workflow_id, new_status):
    """Trigger appropriate function based on status change."""
    if new_status in STATUS_ACTIONS:
        next_step = STATUS_ACTIONS[new_status]
        print(f"Triggering {next_step} step for workflow {workflow_id}.")
        response = run_worker_step(next_step, str(workflow_id)) # Run the corresponding function with sfapi

        # if new_status == "waiting for jobs":
        #     # return # End handle since not watcher's job
        #     print(f'action pending: {new_status}')

        # elif new_status == "generating runs":
        #     # If generate finishes, move on to next status
        #     # update_workflow_status("launching to queue", str(workflow_id))
        #     print(f'action pending: {new_status}')

        # elif new_status == "launching to queue":
        #     # If run finishes, move on to next status
        #     # update_workflow_status("waiting for jobs", str(workflow_id))
        #     print(f'action pending: {new_status}')

        # elif new_status == "writing":   
        #     # If write finishes, move on to next status
        #     print(f'action pending: {new_status}')

        #     print("Pause from watcher.py, implement write.py")

def watch_workflow_status():
    """Watches the workflow collection for status changes."""
    print("Watching workflow collection for status updates...")
    pipeline = [{'$match': {"updateDescription.updatedFields.status": {"$exists": True}}}]
    
    with workflows_collection.watch(pipeline, full_document="updateLookup") as stream:
        for change in stream:
            try:
                workflow_id = change["documentKey"]["_id"]
                new_status = change["updateDescription"]["updatedFields"].get("status")
                if new_status:
                    handle_status_change(workflow_id, new_status)
            except Exception as e:
                print(f"Error handling status change: {e}")

def start_watcher():
    """Start the workflow watcher in a separate thread."""
    watcher_thread = threading.Thread(target=watch_workflow_status, daemon=True)
    watcher_thread.start()
    print("Workflow status watcher started.")

