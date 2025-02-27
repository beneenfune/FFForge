from flask import Flask, request
from flask_restful import Api
from dotenv import load_dotenv
from utils.db import db, ffforge_collection  # Import database and collections
import os
import sys

app = Flask(__name__)
api = Api(app)

# Load .env file explicitly
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

required_env_vars = ["MONGO_URI", "LOCAL_MONGO_URI", "ROOT_DIR", "SFAPI_CLIENT_ID", "SFAPI_SECRET", "SFAPI_PRIVATE_KEY"]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)  # Stop execution

# Route to Check Database Connection
@app.route("/check-db")
def check_db_connection():
    try:
        # List all collections in the database
        collections = db.list_collection_names()
        if collections:
            return {"status": "success", "collections": collections}, 200
        else:
            return {
                "status": "success",
                "message": "Connected to the database but no collections found.",
            }, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

# For CORS
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
    return response

# Additional Routes
import routes
