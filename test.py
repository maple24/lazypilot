import requests

# URL where you want to send the POST request
url = "http://localhost:8000/publish/"

# Data to be sent in the POST request body (as a dictionary)
data = {
    "topic": "webcam",
    "action": {"method": "compare", "params": {"region": "2", "thre": 0.01}},
}
data = {
    "topic": "webcam",
    "action": {"method": "start_cam", "params": {"region": "2", "thre": 0.01}},
}
data = {
    "topic": "webcam",
    "action": {"method": "close_cam", "params": {"region": "2", "thre": 0.01}},
}

# Send the POST request with the data
response = requests.post(url, json=data)

# Check the response
if response.status_code == 200:
    print("Request was successful")
    print("Response:", response.text)
else:
    print("Request failed with status code:", response.status_code)
