import requests
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

# Define the required SCOPES
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Replace 'awesome-dogfish-399811-a7edd8a0f8ce.json' with your service account JSON file name
SERVICE_ACCOUNT_FILE = 'vertexAIcred.json'

# Load credentials from the service account file with the specified SCOPES
cred = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Create an authentication request
auth_req = google.auth.transport.requests.Request()

# Refresh the credentials
cred.refresh(auth_req)

# Obtain the bearer token
bearer_token = cred.token

# Define the base URL for your specific region (us-central1 in this example)
base_url = "https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/us-central1/endpoints/{endpoint_id}:predict"

# Replace 'awesome-dogfish-399811' with your GCP project ID
project_id = "docai-416106"

# Replace '639689267970310144' with the Endpoint ID from the model dashboard
endpoint_id = "898250422358114304"

# Define the request body for your specific prompt and parameters
request_body = {
    "instances": [
        {
            "prompt": "Write a poem about Valencia.",
            "max_length": 200,
            "top_k": 10
        }
    ]
}

# Create the full URL using the project and endpoint IDs
full_url = base_url.format(project_id=project_id, endpoint_id=endpoint_id)

# Define the headers with the bearer token and content type
headers = {
    "Authorization": "Bearer {bearer_token}".format(bearer_token=bearer_token),
    "Content-Type": "application/json"
}

try:
    # Send a POST request to the model endpoint
    resp = requests.post(full_url, json=request_body, headers=headers)
    # Print the response from the model
    print(resp.json())
except Exception as e:
  print("An exception occurred : ",e)