from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os
import ssl

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
    db = client['ffforge_db']
    # Test connection
    client.server_info()  # This forces a connection attempt
except errors.ServerSelectionTimeoutError as e:
    raise ConnectionError("Failed to connect to MongoDB: Server selection timed out. Check the remote IP address.") from e
except ssl.SSLError as e:
    raise ConnectionError("Failed to connect to MongoDB: SSL handshake error. Verify your MongoDB TLS settings or update the remote IP.") from e
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

# Collections
ffforge_collection = db['ffforge_collection']
users_collection = db['users']
workflows_collection = db['workflows']  
