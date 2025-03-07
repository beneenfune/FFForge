from datetime import datetime, timezone

# Define the Workflow model as a dictionary (MongoDB is schema-less)
def create_workflow_entry(data):
    workflow_entry = {
        "prefix": data["prefix"],
        "max_structures": data["max_structures"],
        "purpose": data["purpose"],
        "use_active_learning": data["use_active_learning"],
        "status": "submitted",  
        "created_at": datetime.now(timezone.utc) 
    }

    # Conditionally add fields based on purpose
    if data["purpose"] == "DMA" and "structure_type" in data:
        workflow_entry["structure_type"] = data["structure_type"]
    elif data["purpose"] == "Electrode depletion" and "atom_to_remove" in data:
        workflow_entry["atom_to_remove"] = data["atom_to_remove"]
    elif data["purpose"] == "Electrolyte analysis" and "electrolyte_atoms" in data:
        workflow_entry["electrolyte_atoms"] = data["electrolyte_atoms"]
    elif data["purpose"] == "Adsorption analysis" and "adsorbate_molecules" in data:
        workflow_entry["adsorbate_molecules"] = data["adsorbate_molecules"]

    return workflow_entry
