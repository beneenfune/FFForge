import threading
import pymongo
from bson import ObjectId
from pymongo import MongoClient
from utils.sfapi import run_worker_step
from utils.db import  workflows_collection, update_workflow_status
import os
import asyncio


# Status-action mapping
STATUS_ACTIONS = {
    "generating runs": "generate",
    "launching to queue": "run",
    # "waiting for jobs": "wait",
    # "writing": "write",
}

def handle_status_change(workflow_id, new_status):
    """Trigger appropriate function based on status change."""
    if new_status in STATUS_ACTIONS:
        next_step = STATUS_ACTIONS[new_status]
        print(f"Triggering {next_step} step for workflow {workflow_id}.")
        asyncio.run(run_worker_step(next_step, str(workflow_id)))  # Run the corresponding function
        if new_status == "generating runs":
            update_workflow_status("launching to queue", str(workflow_id))
        elif new_status == "launching to queue":
            print("Pause from watcher.py. Implement run.py")

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

