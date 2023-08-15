import requests


class HTTPRequester:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_request(self, method, endpoint, params=None, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            else:
                return "Invalid HTTP method"

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"


if __name__ == "__main__":
    image_compare = {
        "topic": "webcam",
        "action": {"method": "image_compare", "params": {"region_name": "2", "thre": 0.05}},
    }
    start_cam = {
        "topic": "webcam",
        "action": {"method": "start_cam"},
    }
    stop_cam = {
        "topic": "webcam",
        "action": {"method": "stop_cam"},
    }
    start_video = {
        "topic": "webcam",
        "action": {"method": "start_video"},
    }
    stop_video = {
        "topic": "webcam",
        "action": {"method": "stop_video"},
    }
    base_url = "http://localhost:1234/"
    requester = HTTPRequester(base_url)

    # post_response = requester.send_request("POST", "publish/", data=start_cam)
    # post_response = requester.send_request("POST", "publish/", data=stop_cam)
    # post_response = requester.send_request("POST", "publish/", data=start_cam)
    # post_response = requester.send_request("POST", "publish/", data=start_video)
    # post_response = requester.send_request("POST", "publish/", data=stop_video)
    post_response = requester.send_request("POST", "publish/", data=image_compare)
    print("POST Response:", post_response)
