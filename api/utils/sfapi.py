from sfapi_client import AsyncClient
from sfapi_client.compute import Machine
from sfapi_client import Resource
from authlib.jose import JsonWebKey
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import PrivateKeyJWT
from dotenv import load_dotenv
from io import BytesIO
from .preprocessing import generate_hash
import asyncio
import json
import os
import sys
import requests

# Load environment variables from .env file
load_dotenv()

# Get the credentials from the environment
client_id = os.getenv("SFAPI_CLIENT_ID")
sfapi_secret = os.getenv("SFAPI_SECRET")
private_key= os.getenv("SFAPI_PRIVATE_KEY")
client_secret = JsonWebKey.import_key(json.loads(sfapi_secret))

# Create authenticated session
token_url = "https://oidc.nersc.gov/c2id/token"
session = OAuth2Session(
    client_id, 
    private_key, 
    PrivateKeyJWT(token_url),
    grant_type="client_credentials",
    token_endpoint=token_url
)
session.fetch_token()

async def fetch_status():
    """Fetch and print the status of the Perlmutter machine."""
    async with AsyncClient() as client:
        status = await client.compute(Machine.perlmutter)
        print("Perlmutter Status:")
        print(status)
        print()

async def fetch_outages():
    """Fetch and print the most recent outages for the Spin resource."""
    async with AsyncClient() as client:
        outages = await client.resources.outages(Resource.spin)
        print("Recent Outages for Spin:")
        if outages:
            for outage in outages:
                print(outage)
        else:
            print("No recent outages found.")
        print()

async def upload_file(file_path, target_directory):
    """Upload a file to a specified directory on Perlmutter."""
    async with AsyncClient(client_id, client_secret) as client:
        perlmutter = await client.compute(Machine.perlmutter)

        # List directories to find the target directory
        directories = await perlmutter.ls(target_directory, directory=True)
        if not directories:
            print(f"Directory {target_directory} does not exist on Perlmutter.")
            return

        # Assuming target_directory is valid, proceed with upload
        [target] = directories

        # Open the file as a binary stream
        with open(file_path, "rb") as f:
            file_content = BytesIO(f.read())
            file_content.filename = os.path.basename(file_path)  # Set the filename attribute

            await target.upload(file_content)
            print(f"Uploaded {file_path} to {target_directory} on Perlmutter.")

def create_directory_on_login_node(system_name, root_directory, directory_name=generate_hash()):
    """Create a directory in Perlmutter login node by running a command."""
    
    # Construct the new directory path
    new_directory_path = f"{root_directory}/{directory_name}"

    # Construct the command to make the directory
    cmd = f"mkdir -p {root_directory}/{directory_name}"

    # Define the API endpoint
    api_endpoint = f"https://api.nersc.gov/api/v1.2/utilities/command/{system_name}"

    # Send the POST request with the command
    response = session.post(api_endpoint, data={"executable": cmd})

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get('status') == 'OK':
            print(f"Directory {new_directory_path} created successfully.")
            return new_directory_path
        else:
            print(f"Failed to create directory: {response_data.get('error')}")
            return None
    else:
        print(f"HTTP request failed with status code: {response.status_code}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sfapi.py <file_path> <target_directory>")
        sys.exit(1)

    file_path = sys.argv[1]
    target_directory = sys.argv[2]
    
    if not os.path.isfile(file_path):
        print(f"The file {file_path} does not exist.")
        sys.exit(1)
    
    asyncio.run(upload_file(file_path, target_directory))