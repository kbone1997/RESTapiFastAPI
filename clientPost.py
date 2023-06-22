import requests

# Set the API endpoint URL
url = 'http://127.0.0.1:8000/analyze'

# Prepare the JSON payload
payLoadLines = ["this is a negative line","this is the positive line","I am ok with this task"]
payload = {
    "text": payLoadLines
}

# Send the POST request with JSON payload
response = requests.post(url, json=payload)

# Check the response status code where 200 means connection status ok
if response.status_code == 200:
    # Get the JSON response data
    analysis_result = response.json()

    # Extract sentiment predictions from the analysis result
    sentiment = analysis_result['sentiment']

    # Print the sentiment predictions
    print(f'sentiment : {sentiment}')
else:
    print(f'Request failed with status code: {response.status_code}')
    print(f'Error message: {response.text}')
