from datetime import datetime, timezone

# Define the Workflow model as a dictionary (MongoDB is schema-less)
def create_workflow_entry(data):
    workflow_entry = {
        "prefix": data["prefix"],
        "max_structures": data["max_structures"],
        "purpose": data["purpose"],
        "structure_type": data["structure_type"],
        "use_active_learning": data["use_active_learning"],
        "status": "submitted",  # Initial status
        "created_at": datetime.now(timezone.utc)  # ✅ Correct UTC timestamp
    }
    return workflow_entry
