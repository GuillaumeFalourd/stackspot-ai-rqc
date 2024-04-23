import requests
import time
import json
import os

def save_output(name: str, value: str):
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output_file:
        print(f'{name}={value}', file=output_file)

# Step 1: Authentication to obtain access token
def get_access_token(account_slug, client_id, client_key):
    url = f"https://idm.stackspot.com/{account_slug}/oidc/oauth/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'client_id': client_id,
        'grant_type': 'client_credentials',
        'client_secret': client_key
    }
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data['access_token']

# Step 2: Creation of a Quick Command (RQC) execution
def create_rqc_execution(qc_slug, access_token, input_data):
    url = f"https://genai-code-buddy-api.stackspot.com/v1/quick-commands/create-execution/{qc_slug}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'input_data': input_data
    }

    # print('File data to analyze:', data) 
    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        decoded_content = response.content.decode('utf-8')  # Decode bytes to string
        extracted_value = decoded_content.strip('"')  # Strip the surrounding quotes
        response_data = extracted_value
        print('ExecutionID:', response_data)
        return response_data
    else:
        print(response.status_code)
        print(response.content)

# Step 3: Polling for the execution status
def get_execution_status(execution_id, access_token):
    url = f"https://genai-code-buddy-api.stackspot.com/v1/quick-commands/callback/{execution_id}"
    headers = {'Authorization': f'Bearer {access_token}'}
    i = 0
    while True:
        response = requests.get(
            url, 
            headers=headers
        )
        response_data = response.json()
        status = response_data['progress']['status']
        if status in ['COMPLETED', 'FAILED']:
            return response_data
        else:
            print("Status:", f'{status} ({i})')
            print("Execution in progress, waiting...")
            i+=1
            time.sleep(5)  # Wait for 5 seconds before polling again

# Replace the placeholders with your actual data
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_KEY = os.getenv("CLIENT_KEY")
ACCOUNT_SLUG = os.getenv("CLIENT_REALM")
QC_SLUG = os.getenv("QC_SLUG")
INPUT_DATA = os.getenv("INPUT_DATA")

# Execute the steps
access_token = get_access_token(ACCOUNT_SLUG, CLIENT_ID, CLIENT_KEY)
execution_id = create_rqc_execution(QC_SLUG, access_token, INPUT_DATA)
execution_status = get_execution_status(execution_id, access_token)

# Extract the 'answer' field from the step_result
answer_str = execution_status['steps'][0]['step_result']['answer']

# Remove the leading and trailing ```json and ``` for correct JSON parsing
answer_str = answer_str.strip('`')[4:].strip()

answer_data = json.loads(answer_str)

print(f'\n\033[36mRemote quick command answer:\033[0m \n\n{answer_data}')

save_output('answer', answer_data)

print('\n\033[36mOutput saved successfully!\033[0m')