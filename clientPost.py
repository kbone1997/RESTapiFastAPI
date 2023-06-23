import requests

# Set the API endpoint URL
url = 'http://127.0.0.1:8000/analyze'

# Prepare the JSON payload
# You can check your custom outputs by giving your own line
payLoadLines = ["this is a positive line",""]
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
