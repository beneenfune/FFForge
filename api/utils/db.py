from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Validate and Get Mongo URI
MONGO_URI = os.getenv("LOCAL_MONGO_URI")
if not MONGO_URI:
    raise EnvironmentError("MONGO_URI environment variable must be set in the .env file.")

# Set up MongoDB client
try:
    client = MongoClient(MONGO_URI)
    db = client['ffforge_db'] 
except Exception as e:
    raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

# Collections
ffforge_collection = db['ffforge_collection']  
