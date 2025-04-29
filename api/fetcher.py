# fetcher.py
from __init__ import app
from apscheduler.schedulers.background import BackgroundScheduler
from utils.db import update_workflow_status, get_current_status
from utils.sfapi import get_lpad_wf, get_task

import time
import json

# APScheduler instance
scheduler = BackgroundScheduler()
fetcher_jobs = {}

# Time intervals per status
fetch_intervals = {
    "generating runs": 5,
    "launching to queue": 5,
    "waiting for jobs": 60,  # 1 minute
    "writing": 5,
}

import json

def fetch_and_update(workflow_id):
    """
    Fetch workflow data and update status if conditions are met.
    """
    # Get the current status from the DB
    current_status = get_current_status(workflow_id)
    print(f"[INFO] Fetching workflow {workflow_id} with status '{current_status}'...")

    query_filter = '-fws "READY"'
    fetched_data = get_lpad_wf(workflow_id, query_filter)

    # Check for errors or empty data
    if not fetched_data:
        print(f"[ERROR] Failed to fetch workflow data: {fetched_data.get('error', 'Unknown error')}")
        return

    # Handle both types of responses correctly
    if fetched_data.get("status") == "OK" and "task_id" in fetched_data:
        task_id = fetched_data["task_id"]
        print(f"[INFO] Using task_id: {task_id} from fetched data.")
    elif isinstance(fetched_data, list) and fetched_data:  # Case where parsed JSON is returned
        print("[INFO] Using parsed Fireworks data.")
        task_data = fetched_data
    else:
        print(f"[ERROR] Unexpected format in fetched data: {fetched_data}")
        return

    # If we got a task_id, get the task data
    if "task_id" in locals():
        task_data = get_task(task_id)

        # Validate task_data before continuing
        if not task_data or "error" in task_data:
            print(f"[ERROR] Failed to fetch task data for task_id {task_id}: {task_data.get('error')}")
            return

        # Check if the result key exists and contains a JSON string
        if "result" in task_data and isinstance(task_data["result"], str):
            try:
                # Deserialize the JSON string in result
                task_result = json.loads(task_data["result"])
                print(f"[INFO] Parsed task result: {task_result}")
                
                # Check if 'output' is present and is also a string that needs parsing
                if "output" in task_result and isinstance(task_result["output"], str):
                    task_data = json.loads(task_result["output"])
                    print("[INFO] Successfully parsed task output.")
                else:
                    print(f"[ERROR] Unexpected format in task result: {task_result}")
                    return
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to parse task result: {str(e)}")
                return
        else:
            print(f"[ERROR] No valid 'result' key found in task_data: {task_data}")
            return

    # ✅ task_data is now properly parsed and can be passed to check_continue_condition
    print(f"task_data: {task_data}, (type: {type(task_data)})")

    # Pass the fetched task_data to check_continue_condition
    is_prev_step_finished, next_status = check_continue_condition(task_data, current_status)

    # If the previous step is done and a new status exists, update it
    if is_prev_step_finished and next_status:
        print(f"[INFO] Transitioning from '{current_status}' → '{next_status}'...")
        update_workflow_status(next_status, workflow_id)

        # Stop fetcher if the workflow is complete
        if next_status == "complete":
            print(f"[INFO] Workflow {workflow_id} completed. Stopping fetcher.")
            stop_fetcher(workflow_id)
            return

        # Dynamically adjust interval based on new status
        reschedule_fetcher(workflow_id, next_status)




def check_continue_condition(fetched_data, current_status):
    """
    Check if conditions are met to move to the next step.
    Works with both a single dict or a list of dicts.
    """

    # Normalize to a list of dicts
    if isinstance(fetched_data, dict):
        data_list = [fetched_data]
    elif isinstance(fetched_data, list):
        data_list = fetched_data
    else:
        print(f"[ERROR] Unexpected type for fetched_data: {type(fetched_data)}")
        return False, None

    # Define conditions based on current status
    conditions = {
        "generating runs": lambda data: any(fw.get("state") == "READY" and fw.get("name") == "static" for fw in data),
        "launching to queue": lambda data: len(data) == 0,
        "waiting for jobs": lambda data: any(fw.get("state") == "READY" and fw.get("name") == "store_inputs" for fw in data),
        "writing": lambda data: len(data) == 0,
    }

    next_status_map = {
        "generating runs": "launching to queue",
        "launching to queue": "waiting for jobs",
        "waiting for jobs": "writing",
        "writing": "complete",
    }

    if current_status in conditions and conditions[current_status](data_list):
        return True, next_status_map[current_status]

    return False, None

def reschedule_fetcher(workflow_id, new_status):
    """
    Reschedule the fetcher with a new interval based on status.
    """
    if workflow_id in fetcher_jobs:
        print(f"[INFO] Rescheduling fetcher for workflow {workflow_id} with status '{new_status}'...")
        fetcher_jobs[workflow_id].remove()

    interval = fetch_intervals.get(new_status, 5)
    fetcher_jobs[workflow_id] = scheduler.add_job(
        fetch_and_update,
        "interval",
        seconds=interval,
        args=[workflow_id],
        id=workflow_id,
        replace_existing=True,
    )
    print(f"[INFO] Fetcher rescheduled for workflow {workflow_id} with interval {interval}s.")

def run_fetcher(workflow_id):
    """
    Start the fetcher using APScheduler.
    """
    if workflow_id in fetcher_jobs:
        print(f"[WARNING] Fetcher already running for workflow {workflow_id}.")
        return

    print(f"[INFO] Starting fetcher for workflow {workflow_id}...")
    interval = fetch_intervals["generating runs"]  # Start with initial status interval
    fetcher_jobs[workflow_id] = scheduler.add_job(
        fetch_and_update,
        "interval",
        seconds=interval,
        args=[workflow_id],
        id=workflow_id,
        replace_existing=True,
    )
    print(f"[INFO] Fetcher started for workflow {workflow_id} with interval {interval}s.")
    if not scheduler.running:
        scheduler.start()

def stop_fetcher(workflow_id):
    """
    Stop the fetcher for a given workflow ID.
    """
    if workflow_id in fetcher_jobs:
        print(f"[INFO] Stopping fetcher for workflow {workflow_id}...")
        fetcher_jobs[workflow_id].remove()
        del fetcher_jobs[workflow_id]
        print(f"[INFO] Fetcher for workflow {workflow_id} has been stopped.")
    else:
        print(f"[WARNING] No fetcher running for workflow {workflow_id}.")
