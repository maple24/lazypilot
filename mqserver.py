import zmq
import time

context = zmq.Context()

# Create a PUB socket
publisher = context.socket(zmq.PUB)
publisher.bind("tcp://*:5556")

while True:
    topic = b"weather"
    message = b"Today's weather forecast: Sunny!"
    publisher.send_multipart([topic, message])
    time.sleep(1)
