# lazypilot

## architecture
- zeroMQ to publish message to processes with [topic, message]
- multiprocessing queue to get response back
- fastapi to provide restapi interface

## test
curl -X POST -H "Content-Type: application/json" -d '{"message": "Your message here"}' http://localhost:8000/update_message/

curl -X POST http://localhost:8000/publish/YourMessageHere