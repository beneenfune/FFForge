from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
import ssl
from bson import ObjectId

# Load environment variables from .env
load_dotenv()

# Validate and Get Mongo URI
MONGO_URI = os.getenv("REMOTE_MONGO_URI")
# MONGO_URI = os.getenv("LOCAL_MONGO_URI")

if not MONGO_URI:
    raise EnvironmentError("MONGO_URI environment variable must be set in the .env file.")

# Set up MongoDB client
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # 5s timeout
    # Test connection
    client.server_info()  # This forces a connection attempt
except errors.ServerSelectionTimeoutError as e:
    raise ConnectionError("Failed to connect to MongoDB: Server selection timed out. Check the remote IP address.") from e
except ssl.SSLError as e:
    raise ConnectionError("Failed to connect to MongoDB: SSL handshake error. Verify your MongoDB TLS settings or update the remote IP.") from e
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

db = client['ffforge_db']


# Collections
ffforge_collection = db['ffforge_collection']
users_collection = db['users']
workflows_collection = db['workflows']  

# Functions
def update_workflow_status(new_status, workflow_id):
    """Update the status of a workflow in the database.

    Args:
        workflow_id (str): The ID of the workflow to update.
        new_status (str): The new status to set.

    Returns:
        dict: The updated workflow document or None if not found.
    """
    result = workflows_collection.find_one_and_update(
        {"_id": ObjectId(workflow_id)},
        {"$set": {"status": new_status}},
        return_document=True  # Return the updated document
    )

    return {
        "status" : new_status
    }