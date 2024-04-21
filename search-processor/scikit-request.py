import requests

# Define the data to be sent in JSON format
data = {'query': 'componet lokic'}

# Make a POST request to the Flask server
response = requests.post('http://127.0.0.1:5000/search-scikit', json=data)

if response.status_code == 400:
    print("Bad request: ", response.text)
else:
    print(response.json())
